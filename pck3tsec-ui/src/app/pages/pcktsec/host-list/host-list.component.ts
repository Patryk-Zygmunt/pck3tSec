import { Component, OnInit } from '@angular/core';

import {Host} from "../../../_model/model";
import {HostsService} from "../../../_service/hosts.service";
import {NbDialogService} from "@nebular/theme";
import {PcktsecListComponent} from "../pcktsec-list";

@Component({
  selector: 'ngx-host-list',
  templateUrl: './host-list.component.html',
  styleUrls: ['./host-list.component.scss']
})
export class HostListComponent  extends PcktsecListComponent implements OnInit {
  hosts: Host[] = []


  constructor( protected  hostService:HostsService, protected dialogService: NbDialogService) {
    super(hostService,dialogService);
  }
  ngOnInit(): void {
    this.hostService.getHosts()
      .subscribe(res=>this.hosts=res)
  }

}
