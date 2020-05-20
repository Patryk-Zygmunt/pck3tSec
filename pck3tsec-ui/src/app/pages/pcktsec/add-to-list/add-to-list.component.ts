import {Component, Input, OnInit} from '@angular/core';
import {NbDialogRef} from "@nebular/theme";
import {Host, HostList} from "../../../_model/model";
import {HostsService} from "../../../_service/hosts.service";

@Component({
  selector: 'ngx-add-to-list',
  templateUrl: './add-to-list.component.html',
  styleUrls: ['./add-to-list.component.scss']
})
export class AddToListComponent {



  @Input()
  set host(host){
    console.log(host)
    this._host.host = host.id;

    if(host.host_source){
      this._host.host = host.host_source.id;
    }


  }


  _host:any = {};
  reason: any;

  constructor(protected ref: NbDialogRef<AddToListComponent>,private hostService:HostsService) {}



  addToBlackList(){
    this._host.reason = this.reason;
    this.hostService.addToBlackList(this._host)
      .subscribe(()=>this.ref.close())
  }


  addToWhiteList(){
    this._host.reason = this.reason;
    this.hostService.addToWhiteList(this._host)
      .subscribe(()=>this.ref.close())
  }



}
