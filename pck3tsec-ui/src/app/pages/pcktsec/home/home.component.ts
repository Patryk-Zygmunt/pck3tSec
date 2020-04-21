import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'ngx-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {


  recordTraffic = {
    title: 'Recording traffic',
    icon: 'fas fa-signal',
    type: 'info',
  };

  detectThreats = {
    title: 'Detecting threats',
    icon: 'fas fa-exclamation-triangle',
    type: 'warning',
  };

  checkWhitelist = {
    title: 'Check Whitelist',
    icon: 'far fa-check-square',
    type: 'success',
  };

  checkBlacklist = {
    title: 'Check Blacklist',
    icon: 'fas fa-ban',
    type: 'danger',
  };

  checkNotification = {
    title: 'Notifications',
    icon: 'far fa-bell',
    type: 'primary',
  };



  constructor() { }

  ngOnInit(): void {
  }

}
