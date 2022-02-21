import { Injectable } from '@angular/core';
import { HttpClient, HttpRequest } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  private apiBaseUrl = environment.apiBaseUrl;

  constructor(private http: HttpClient) { }

  getSampleImages(): any {
    return this.http.get(this.apiBaseUrl + "/sample/images");
  }

  submitImageFile(fileFormData: FormData): any {

    const req = new HttpRequest(
      'POST',
      this.apiBaseUrl + '/upload/image',
      fileFormData,
      {
        reportProgress: true,
      }
    );
    return this.http.request(req);
  }
}
