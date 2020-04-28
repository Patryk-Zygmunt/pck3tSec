import { Component, OnInit } from '@angular/core';
import {HostsService} from "../../../_service/hosts.service";
import {NbDialogService} from "@nebular/theme";
import {PcktsecListComponent} from "../pcktsec-list";
import {HostList} from "../../../_model/model";

@Component({
  selector: 'ngx-blacklist',
  templateUrl: './blacklist.component.html',
  styleUrls: ['./blacklist.component.scss']
})
export class BlacklistComponent extends PcktsecListComponent implements OnInit {

  hosts:HostList[] = []

  constructor( protected  hostService:HostsService, protected dialogService: NbDialogService) {
    super(hostService,dialogService);
  }

  ngOnInit(): void {
   this.fetchList()
  }
  fetchList(){
    this.hostService.getBlackList()
      .subscribe(res=>this.hosts=res)
  }

  remove(host){
    this.hostService.deleteFromBlacklist(host.id)
      .subscribe(()=>this.fetchList())

  }

}
