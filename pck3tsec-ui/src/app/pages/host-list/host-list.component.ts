import { Component, OnInit } from '@angular/core';
import {NbThemeService} from "@nebular/theme";
import {takeWhile} from "rxjs/operators";

@Component({
  selector: 'ngx-host-list',
  templateUrl: './host-list.component.html',
  styleUrls: ['./host-list.component.scss']
})
export class HostListComponent implements OnInit {
  items=[{date:4,value:4}]
  private alive = true;
  currentTheme: string;

  constructor(private themeService: NbThemeService) {
    this.themeService.getJsTheme()
      .pipe(takeWhile(() => this.alive))
      .subscribe(theme => {
        this.currentTheme = theme.name;
      });
  }
  ngOnInit(): void {
  }

}
