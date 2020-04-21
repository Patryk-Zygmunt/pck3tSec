import { NgModule } from '@angular/core';
import {NbButtonModule, NbCardModule, NbIconModule, NbInputModule, NbListModule, NbMenuModule} from '@nebular/theme';

import { ThemeModule } from '../@theme/theme.module';
import { PagesComponent } from './pages.component';

import { PagesRoutingModule } from './pages-routing.module';
import {HostListComponent} from "./pcktsec/host-list/host-list.component";
import {HttpClientModule} from "@angular/common/http";
import { AddToListComponent } from './pcktsec/add-to-list/add-to-list.component';
import {FormsModule} from "@angular/forms";
import { BlacklistComponent } from './pcktsec/blacklist/blacklist.component';
import {CommonModule} from "@angular/common";
import { WhitelistComponent } from './pcktsec/whitelist/whitelist.component';
import { ThreatsComponent } from './pcktsec/threats/threats.component';
import { HomeComponent } from './pcktsec/home/home.component';
import { ListCardComponent } from './pcktsec/list-card/list-card.component';
import { ThreatsChartComponent } from './pcktsec/threats-chart/threats-chart.component';
import {ChartModule} from "angular2-chartjs";
import { PieChartComponent } from './pcktsec/pie-chart/pie-chart.component';

@NgModule({
  imports: [
    CommonModule,
    ThemeModule,
    PagesRoutingModule,
    NbMenuModule,
    NbListModule,
    NbCardModule,
    NbButtonModule,
    NbInputModule,
    FormsModule,
    NbIconModule,
    ChartModule,

  ],
  declarations: [
    PagesComponent,
    HostListComponent,
    AddToListComponent,
    BlacklistComponent,
    WhitelistComponent,
    ThreatsComponent,
    HomeComponent,
    ListCardComponent,
    ThreatsChartComponent,
    PieChartComponent
  ],
})
export class PagesModule {
}
