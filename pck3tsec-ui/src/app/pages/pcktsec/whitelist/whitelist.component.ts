import { Component, OnInit } from '@angular/core';
import {PcktsecListComponent} from "../pcktsec-list";
import {HostList} from "../../../_model/model";
import {HostsService} from "../../../_service/hosts.service";
import {NbDialogService} from "@nebular/theme";

@Component({
  selector: 'ngx-whitelist',
  templateUrl: './whitelist.component.html',
  styleUrls: ['./whitelist.component.scss']
})
export class WhitelistComponent extends PcktsecListComponent implements OnInit {

  hosts:HostList[] = []

  constructor( protected  hostService:HostsService, protected dialogService: NbDialogService) {
    super(hostService,dialogService);
  }

  ngOnInit(): void {
    this.fetchList()
  }
  fetchList(){
    this.hostService.getWhiteList()
      .subscribe(res=>this.hosts=res)
  }

  remove(host){
    this.hostService.deleteFromWhitelist(host.id)
      .subscribe(()=>this.fetchList())

  }

}
