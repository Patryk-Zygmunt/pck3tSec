import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';

import { PagesComponent } from './pages.component';

import {HostListComponent} from "./pcktsec/host-list/host-list.component";
import {BlacklistComponent} from "./pcktsec/blacklist/blacklist.component";
import {WhitelistComponent} from "./pcktsec/whitelist/whitelist.component";
import {ThreatsComponent} from "./pcktsec/threats/threats.component";
import {HomeComponent} from "./pcktsec/home/home.component";

const routes: Routes = [{
  path: '',
  component: PagesComponent,
  children: [

    {
      path: 'traffic',
      component: HostListComponent,
    },

    {
      path: 'blacklist',
      component: BlacklistComponent,
    },

    {
      path: 'whitelist',
      component: WhitelistComponent,
    },
    {
      path: 'threats',
      component: ThreatsComponent,
    },
    {
      path: '',
      component: HomeComponent,
    },
  ],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class PagesRoutingModule {
}
