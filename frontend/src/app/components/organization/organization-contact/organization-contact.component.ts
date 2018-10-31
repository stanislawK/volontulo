import { Component, OnInit, OnChanges, SimpleChanges, EventEmitter, Output, Input } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { Observable } from 'rxjs/Observable';
import { filter, take } from 'rxjs/operators';

import { OrganizationContactPayload, ContactStatus } from 'app/models/organization.model';
import { AuthService } from 'app/services/auth.service';
import { User } from 'app/models/user.model';
import { UserService } from 'app/services/user.service';

@Component({
  selector: 'volontulo-organization-contact',
  templateUrl: './organization-contact.component.html',
  styleUrls: ['./organization-contact.component.scss']
})

export class OrganizationContactComponent implements OnInit, OnChanges {
  @Input() contactStatus: ContactStatus;
  @Output() contact = new EventEmitter<OrganizationContactPayload>();
  submitDisabled = false;
  user$: Observable<User> = this.authService.user$;
  getFullName = this.userService.getFullName;

  public fg: FormGroup = this.fb.group({
    name: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(30)]],
    email: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(30), Validators.email]],
    phone_no: ['', [Validators.required, Validators.minLength(9), Validators.maxLength(9), Validators.pattern(/^[0-9]{9}$/)]],
    message: ['', [Validators.required, Validators.minLength(10), Validators.maxLength(2000)]],
    honeyBunny: ['']
  });
  public success: null | boolean = null;


  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private userService: UserService
  ) { }

  ngOnInit() {
    this.user$
    .pipe(
      filter(user => user !== null),
      take(1),
    )
    .subscribe(user => {
      this.fg.controls.name.setValue(this.getFullName(user));
      this.fg.controls.email.setValue(user.email);
      this.fg.controls.phone_no.setValue(user.phoneNo);
      });
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes.contactStatus.currentValue && changes.contactStatus.currentValue.status === 'success') {
      this.success = true;
      this.fg.controls.message.reset();
    } else if (changes.contactStatus.currentValue && changes.contactStatus.currentValue.status === 'error') {
      this.success = false;
    }
    this.submitDisabled = false;
  }

  onSubmit() {
    if (this.fg.valid && !this.fg.value.honeyBunny) {
      this.submitDisabled = true;
      delete this.fg.value.honeyBunny;
      this.contact.emit(this.fg.value as OrganizationContactPayload);
    }
 }
}
