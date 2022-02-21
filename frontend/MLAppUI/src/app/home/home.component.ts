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

    let data = {
      "images": [{
        "img_name": "CNV-1016042-1.jpeg",
        "class": "CNV",
        "img_path": "/assets/test_images/CNV-1016042-1.jpeg",
        "prediction_img_path": "/assets/test_images/CNV-1016042-1-overlay.jpeg"
      }, {
        "img_name": "DME-1081406-1.jpeg",
        "class": "DME",
        "img_path": "/assets/test_images/DME-1081406-1.jpeg",
        "prediction_img_path": "/assets/test_images/DME-1081406-1-overlay.jpeg"
      }, {
        "img_name": "DRUSEN-1083159-1.jpeg",
        "class": "DRUSEN",
        "img_path": "/assets/test_images/DRUSEN-1083159-1.jpeg",
        "prediction_img_path": "/assets/test_images/DRUSEN-1083159-1-overlay.jpeg"
      }, {
        "img_name": "NORMAL-1017237-1.jpeg",
        "class": "NORMAL",
        "img_path": "/assets/test_images/NORMAL-1017237-1.jpeg",
        "prediction_img_path": "/assets/test_images/NORMAL-1017237-1-overlay.jpeg"
      }]
    };

    this.sampleImages = data.images;

    // this.dataService.getSampleImages().subscribe((data: { images: any; }) => {
    //   this.sampleImages = data.images;
    // });
  }

}
