import {OnInit} from "@angular/core";
import {Host} from "../../_model/model";
import {HostsService} from "../../_service/hosts.service";
import {NbDialogService} from "@nebular/theme";
import {AddToListComponent} from "./add-to-list/add-to-list.component";

export class PcktsecListComponent {


  constructor(protected  hostService:HostsService, protected dialogService: NbDialogService) {
  }

  addToList(host){
      this.dialogService.open(AddToListComponent, {
        context: {
          host: host,
        },
      });
  }

}
