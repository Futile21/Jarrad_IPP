import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { PlottingComponent } from './plotting/plotting.component';


import { PlotlyViaCDNModule } from './plotly-via-cdn/plotly-via-cdn.module';
PlotlyViaCDNModule.plotlyVersion = '1.49.4';

// import { PlotlyModule } from './plotly/plotly.module';
// import * as PlotlyJS from 'plotly.js/dist/plotly.js';
// PlotlyModule.plotlyjs = PlotlyJS;

// import * as PlotlyJS from 'plotly.js/dist/plotly.js';
// import { PlotlyModule } from 'angular-plotly.js';

// PlotlyModule.plotlyjs = PlotlyJS;

@NgModule({
  declarations: [
    AppComponent,
    PlottingComponent
  ],
  imports: [
    BrowserModule,
    PlotlyViaCDNModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
