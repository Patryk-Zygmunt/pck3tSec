import { NgModule } from '@angular/core';
import {NbCardModule, NbListModule, NbMenuModule} from '@nebular/theme';

import { ThemeModule } from '../@theme/theme.module';
import { PagesComponent } from './pages.component';
import { DashboardModule } from './dashboard/dashboard.module';
import { ECommerceModule } from './e-commerce/e-commerce.module';
import { PagesRoutingModule } from './pages-routing.module';
import { MiscellaneousModule } from './miscellaneous/miscellaneous.module';
import {HostListComponent} from "./host-list/host-list.component";

@NgModule({
  imports: [
    ThemeModule,
    PagesRoutingModule,
    ThemeModule,
    NbMenuModule,
    DashboardModule,
    ECommerceModule,
    MiscellaneousModule,
    NbListModule,
    NbCardModule,

  ],
  declarations: [
    PagesComponent,
    HostListComponent
  ],
})
export class PagesModule {
}
