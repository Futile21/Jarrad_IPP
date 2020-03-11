import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
declare var Plotly: any;

@Component({
  selector: 'app-plotting',
  templateUrl: './plotting.component.html',
  styleUrls: ['./plotting.component.css']
})
export class PlottingComponent implements OnInit {

  datalist = [
    {
      x: [1, 2, 3, 4, 5],
      y: [2, 3, 4, 6, 7],
      type: 'scattergl',
      mode: 'lines',
      name: 'Lines'
    }];
  public debug = true;
  public useResizeHandler = true;
  public powerGraph = {
    data : this.datalist,
    layout: {
      tilte: 'test',
    }
  };
  constructor() { }

  // @ViewChild('Graph', { static: true })   private Graph: ElementRef;

  ngOnInit() {
  }
  // @ViewChild('serverContentInput', {static: true}) serverContentInput: ElementRef;

}
