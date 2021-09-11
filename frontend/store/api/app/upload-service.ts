import {SERVER_API_ROUTES} from "~/store/api/routes";
import AxiosService from "~/store/api/axios-service";
import {Status} from "~/store/model/shared";
import {UIFetchStatus} from "~/store/modules/app/todo-store";
import {SignedUploadUrlGetResult, UploadObject, UploadObjectField} from "~/store/model/app/upload";
import {$axios} from "~/utils/api";

export default class UploadService extends AxiosService {

  async getSignedUploadUrl(status: UIFetchStatus = UIFetchStatus.ALL): Promise<SignedUploadUrlGetResult> {
    return super.genericFetch(SERVER_API_ROUTES.ROUTE_UPLOAD,
      new SignedUploadUrlGetResult(new UploadObject("", new UploadObjectField()), new Status()),
      {status: status})
  }

  /**
   * Upload form data directly to S3 object, upload data is POST-ed to pre-signed S3 URL
   *
   * @param signedUploadUrlResult pre-signed url and fields required to be submitted with file data in upload request
   * @param formData form data object with file data
   */
  async uploadS3Post(signedUploadUrlResult: SignedUploadUrlGetResult, formData: FormData) {
    let upload: UploadObject = signedUploadUrlResult.upload
    return $axios.post(upload.url, formData, {})
  }

}
