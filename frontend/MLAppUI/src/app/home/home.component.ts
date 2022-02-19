import { Component, OnInit } from '@angular/core';
import { DataService } from '../services/data.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  sampleImages: any;

  constructor(private dataService: DataService) { }

  ngOnInit(): void {
    this.dataService.getSampleImages().subscribe((data: { images: any; }) => {
      this.sampleImages = data.images;
    });
  }

}
