import { HttpEventType, HttpHeaderResponse, HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { finalize } from 'rxjs/operators';
import { DataService } from '../services/data.service';

@Component({
  selector: 'app-demo',
  templateUrl: './demo.component.html',
  styleUrls: ['./demo.component.scss']
})
export class DemoComponent implements OnInit {
  selectedFile: File | any;
  errorMsg: string = '';
  uploadProgress: number = 0;
  uploading: boolean = false;
  submissionResult: any;
  category: any;
  overlayFileName: any;
  imgFile: string = '';
  sampleImages: any[] = [];
  showSamples: boolean = false;

  constructor(private dataService: DataService) { }

  ngOnInit(): void {
    this.getSampleFiles();
  }

  chooseFile(files: FileList | null) {
    this.submissionResult = null;
    this.category = null;
    this.overlayFileName = null;

    this.selectedFile = null;
    this.errorMsg = '';
    this.uploadProgress = 0;
    if (!files || files.length === 0) {
      return;
    }
    this.selectedFile = files[0];


    const reader = new FileReader();
    reader.readAsDataURL(this.selectedFile);
    
      reader.onload = () => {
        this.imgFile = reader.result as string;       
      }
  }

  upload() {
    if (!this.selectedFile) {
      this.errorMsg = 'Please choose a file.';
      return;
    }

    const formData = new FormData();
    formData.append('file', this.selectedFile);


    this.uploading = true;
    this.dataService.submitImageFile(formData)
      .pipe(
        finalize(() => {
          this.uploading = false;
          this.selectedFile = null;
        })
      )
      .subscribe(
        (event: { type: any; loaded: number; total: number; body: any; }) => {
          //console.log(event);
          if (event.type === HttpEventType.UploadProgress) {
            console.log(event);
            this.uploadProgress = Math.round(
              (100 * event.loaded) / event.total
            );
          } else if (event instanceof HttpResponse) {
            console.log(event);
            this.submissionResult = event.body;

            if (event.body?.data) {
              this.category = event.body.data.category;
              this.overlayFileName = event.body.data.predicted_output;
            }


          } else if (event instanceof HttpHeaderResponse) {
            console.log(event);
            this.submissionResult = event.body;
          }
          else if (event.body) {
            console.log(event);
            this.submissionResult = event.body;
          }
          else {
            console.log(event);
          }
        },
        (error: any) => {
          // Here, you can either customize the way you want to catch the errors
          throw error; // or rethrow the error if you have a global error handler
        }
      );
  }

  humanFileSize(bytes: number): string {
    if (Math.abs(bytes) < 1024) {
      return bytes + ' B';
    }
    const units = ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    let u = -1;
    do {
      bytes /= 1024;
      u++;
    } while (Math.abs(bytes) >= 1024 && u < units.length - 1);
    return bytes.toFixed(1) + ' ' + units[u];
  }

  getSampleFiles() {

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
  }


}
