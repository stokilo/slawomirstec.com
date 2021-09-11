<template>
  <b-tabs nav-class="separator-tabs ml-0 mb-5" content-class="tab-content" :no-fade="true">
    <b-tab title="S3 file upload and integration with the Cloudflare CDN">
      <div>
        <b-row>
          <b-card class="mb-4" no-body>
            <ResizeImageTag resizeTo=1200 src="blog/2021/01/s3.jpg"
                            class-name="responsive border-0 card-img-top mb-3" alt="S3"/>
            <span
              class="badge badge-pill badge-theme-2 position-absolute badge-top-left">Profile</span>
            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">User profile with file upload feature</h3>
                <p>
                  This is a post about the new functionality added to the sample application. It is a user settings page
                  with an option to upload a profile picture. Every new account gets assigned a default picture.
                  After the login, the user can see it on the right side of the navigation bar. In the utils submenu, user can
                  access a form to change his name and a file upload to update his picture.
                  That is a description of the feature from the user's perspective.
                </p>
                <p></p>
                <p>
                  My motivation to implement this feature was the lack of S3 integration in the sample application.
                  This is probably one of the most important services in AWS, I wanted to add it to the CDK provisioning
                  process and integrate with the UI.
                </p>
                <p>
                  What I quickly realized was that I shouldn't process upload through the Lambda function.
                  My Lambda sits behind API Gateway, and there is a limit for the ApiGateway payload size set to 10 MB. I wanted to
                  reuse the code to upload larger files in the future. And I already know that there is a cheaper option described below.
                </p>
                <p>
                  The solution for this problem was uploading to S3 directly. AWS optimized file upload to S3 buckets and Lambda
                  execution is not required for it. That is why I mentioned there exists a cheaper solution.
                </p>
                <p>
                  Files stored in the S3 buckets are private by default. For file upload, there is a solution
                  to generate a pre-signed URL to the S3 bucket and allow any user to write to it. It is really *any* user. In my case, it is
                  restricted to the authenticated user of the sample application.
                  Pre-signed URL has defined timeout value (i.e. 5 minutes) and after that becomes invalid.
                </p>
                <p>
                  This was what I needed but I didn't want to expose the S3 bucket to the public and allow reads for all users.
                  I decided to add Cloudflare CDN to the mix. I allow all authenticated users to do the uploads which are bucket write action.
                  However, I restricted users to forbid them to see other user's uploads.
                  Additionally, I wanted to have images served by Cloudflare CDN to save some money here.
                </p>
                <p>
                  I succeed almost in all cases except Cloudflare CDN assets protection, more details below.
                </p>
              </div>

              <hr/>

              <div class="mb-5">
                <h3 class="card-title">Cloudflare setup</h3>
                <p>
                  All new accounts will get assigned a default profile picture. URL looks like below:
                </p>
                <p><strong>https://<span style="color: red">img.your-domain.com</span>/default_assets/default_profile_image.png</strong></p>
                <p>
                  I created single S3 bucket with name: <span style="color:red">img.slawomirstec.com</span> and copied
                  default image <strong>/default_assets/default_profile_image.png</strong> there. Bucket and default
                  image deployment is provisioned by CDK, I automatically create it during infrastructure setup.
                  However I don't serve images from a bucket directly, I don't serve it via AWS Cloudfront either.
                  I decided to use the Cloudflare CDN.
                </p>
                <p>
                  Cloudflare cache validity is set to 24 hours. I configured S3 to allow reads from Cloudflare IP addresses only.
                  To have this setup working I had to change my domain DNS and add CNAME record
                </p>
                  <p>
                  CNAME: img <br/>
                  value: img.slawomirstec.com.s3.{my-region}.amazonaws.com
                  </p>
                <p>
                  where my-region is replaced with the region where I host the app.
                </p>
                <p>
                  As a result, the content of my S3 bucket is served via CDN.
                  This is pretty simple. Images are served via CDN, S3 read can be done by Cloudflare only, and it is a cached
                  read, this saves me some money and I don't have to setup Cloudfront on the AWS side. Bucket writes are
                  allowed for all authenticated users and performed directly on the S3 bucket pre-signed URL.
                </p>

              </div>
              <hr/>
              <div class="mb-5">
                <h3 class="card-title">S3 CDK setup</h3>
                <p>
                I started with provisioning the S3 bucket. Bucket name must match CNAME set on Cloudflare side,
                in this case  <span style="color: red">img.slawomirstec.com</span>
                </p>
                <p>
                  I construct this dynamically using environment variables because I support different domains as deployment targets.
                  The subdomain is configurable and by default is equal to the string 'img'.
                </p>
                <p>
                  The next step is the creation of the bucket itself. I set it as non-public and delete it when the infrastructure
                  is destroyed. Additionally, I set CORS rules. When you compare it with the creation of the bucket using
                  AWS Console, this is very similar, here I can do in the code directly. I found one issue with CDK
                  and S3, it is not possible to delete a non-empty bucket. I had to do it from AWS CLI, luckily I
                  do it already with PyAWS CLI so this was not a big issue to add this step.
                </p>
                <p>
                  After that, I set a policy to allow reads only for Cloudflare IP addresses. This is set to
                  AnyPrincipal() that access my configured image domain. Effectively bucket becomes public on
                  the S3 Console! AWS documentation states that public buckets are not recommended, they should be
                  accompanied by access restriction condition. I defined the condition for CDN access and for s3:GetObject action only.
                </p>
                <p>
                  The last step copies default images and deploys them into a newly created bucket.
                </p>
                <p>
                  I did one more change that is not visible in the code below. I had to assign AWS managed policy
                  'AmazonS3FullAccess' to the Lambda role. It was required for the generation of pre-signed URLs from Lambda.
                  I could not find why I needed to assign full s3 access to make it work, it worked locally with Chalice.
                  I guess this is boto3 specific. When boto3 was executed locally, AWS credentials were used from the user directory.
                  On AWS premise this policy was required.
                </p>

                <client-only>
                  <highlightjs langugage="python" :code="snippet1"/>
                </client-only>

              </div>

              <hr/>

              <div class="mb-5">
                <h3 class="card-title">Client changes</h3>
                <p>
                  On the client side, I implemented two functions. First one <strong>getSignedUploadUrl</strong>,
                  calls the backend to request a pre-signed URL. In the response, I receive an upload object with a URL
                  to call (POST) and fields that I have to include in the form data. Second function <strong>uploadS3Post</strong>
                  post form data directly to the S3 URL.
                </p>
                <client-only>
                  <highlightjs langugage="javascript" :code="snippet2"/>
                </client-only>
                <p>Model:</p>
                <client-only>
                  <highlightjs langugage="javascript" :code="snippet3"/>
                </client-only>
                <p></p>
                <p>
                  My fronted stack consists of Vue+TypeScript and Nuxt framework. I converted fields received
                  with the pre-signed URL to form data object. In Typescript it can be easily done using DOM API
                  and File/FormData interfaces.
                </p>
              </div>
              <hr/>

              <div class="mb-5">
                <h3 class="card-title">Backend</h3>
                <p>
                 Upload service autogenerates path for each stored profile picture. I stored year/month/day/hour
                  in the path for easier debugging. The filename gets a random UUID name assigned.
                </p>
                <p>
                  For the pre-signed URL, I defined the maximum size limit to 1MB. Timeout is set to 60 seconds and
                  the bucket name is generated from environment variables.
                </p>
                <p>As expected, there is no code required for S3 upload.</p>
                <client-only>
                  <highlightjs langugage="python" :code="snippet4"/>
                </client-only>
              </div>
              <hr/>

              <div class="mb-5">
                <h3 class="card-title">Cloudflare token authentication</h3>
                <p>
                  I wanted to implement Cloudflare token authentication as described here:
                </p>
                <span>
                  <a href="https://support.cloudflare.com/hc/en-us/articles/115001376488-Configuring-Token-Authentication" rel="noopener noreferrer" target="_blank">https://support.cloudflare.com/hc/en-us/articles/115001376488-Configuring-Token-Authentication</a>
                </span>
                <p></p>
                <p>
                  but I could not get it in a Cloudflare free plan that I use. I wanted to use it to ensure that
                  users can't see other user's uploads. For time being, I had to rely on UUID and HTTPS protocol to hide this information.
                  Cloudflare token authentication looks like a great addition, by defining shared secret on Cloudflare
                  and AWS side, I can create a token that is validated on each GET request. It may look like
                  nothing special but please note that in this scenario, I don't have to run any Lambda function to
                  validate user JWT or implement new Lambda on the Cloudfront Edge to check access rights.
                  Anyway, I will check this in the future and configure it just to play around with it, documentation is
                  very good so it should not take much time to do it.
                </p>
              </div>

            </b-card-body>
          </b-card>
        </b-row>
      </div>
    </b-tab>
  </b-tabs>
</template>

<script lang="ts">
import Component from "vue-class-component";
import Vue from "vue";
import Colxx from '~/components/common/Colxx.vue'
import ResponsiveImageTag from '~/components/common/ResponsiveImageTag.vue'
import ResizeImageTag from "~/components/common/ResizeImageTag.vue";

@Component({
  components: {
    ResizeImageTag,
    ResponsiveImageTag,
    Colxx
  },
  head: {
    title: 'S3 file upload and integration with the Cloudflare CDN',
    meta: [
      {hid: 'description', name: 'description', content: 'How upload directly to AWS S3 bucket and user Cloudflare CDN.'},
      {
        hid: 'keywords',
        name: 'keywords',
        content: 'AWS, S3, file, upload, Cloudflare, CDN, profile, picture'
      }
    ]
  }
})
export default class S3FileUpload extends Vue {
  snippet1: String = `
pyaws_domain = os.environ['PYAWS_CLI_DOMAIN']
pyaws_image_subdomain = os.environ['PYAWS_CLI_IMAGE_SUBDOMAIN']
pyaws_img_domain = f"{pyaws_image_subdomain}.{pyaws_domain}"
img_bucket = Bucket(self, pyaws_img_domain,
                    bucket_name=pyaws_img_domain,
                    public_read_access=False,
                    removal_policy=RemovalPolicy.DESTROY,
                    access_control=BucketAccessControl.AUTHENTICATED_READ,
                    cors=[CorsRule(allowed_methods=[HttpMethods.GET, HttpMethods.POST],
                                   allowed_headers=[],
                                   allowed_origins=[f"https://{pyaws_domain}", "http://localhost:3000"])]
                   )

img_bucket.add_to_resource_policy(permission=PolicyStatement(
    sid=f"policy.cloudflare.sid.{pyaws_img_domain}",
    effect=Effect.ALLOW,
    principals=[AnyPrincipal()],
    actions=["s3:GetObject"],
    resources=[f"arn:aws:s3:::{pyaws_img_domain}/*"],
    conditions={"IpAddress": {"aws:SourceIp": [
        "173.245.48.0/20",
        "103.21.244.0/22",
        "103.22.200.0/22",
        "103.31.4.0/22",
        "141.101.64.0/18",
        "108.162.192.0/18",
        "190.93.240.0/20",
        "188.114.96.0/20",
        "197.234.240.0/22",
        "198.41.128.0/17",
        "162.158.0.0/15",
        "172.64.0.0/13",
        "131.0.72.0/22",
        "104.16.0.0/13",
        "104.24.0.0/14"
    ]
    }}
))

BucketDeployment(self, id="assetsDeployment",
                 sources=[Source.asset('./assets')],
                 destination_bucket=img_bucket)
   `

  snippet2: string = `
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
  `

  snippet3: String = `
export class UploadObjectField {
  public key: string
  public policy: string
  public 'x-amz-algorithm': string
  public 'x-amz-credential': string
  public 'x-amz-date': string
  public 'x-amz-signature': string

  constructor(key: string = "", policy: string = "", x_amz_algorithm: string = "", x_amz_credential: string = "",
              x_amz_date: string = "", x_amz_signature: string = "") {
    this.key = key;
    this.policy = policy;
    this["x-amz-algorithm"] = x_amz_algorithm;
    this["x-amz-credential"] = x_amz_credential;
    this["x-amz-date"] = x_amz_date;
    this["x-amz-signature"] = x_amz_signature;
  }
}

export class UploadObject {
  public url: string
  public fields: UploadObjectField

  constructor(url: string, fields: UploadObjectField) {
    this.url = url;
    this.fields = fields;
  }
}

export class SignedUploadUrlGetResult extends WithFromJson{
  public upload: UploadObject
  public status: Status

  constructor(upload: UploadObject, status: Status) {
    super();
    this.upload = upload
    this.status = status;
  }
}

  `

  snippet4: String = `
import uuid

import boto3
from chalicelib import logger
from chalicelib.model.constants import AWSConstants
from chalicelib.model.shared import Status
from chalicelib.model.upload import SignedUploadUrlResponse
import datetime


class UploadService:

    def __init__(self) -> None:
        pass

    def created_signed_url_profile_update(self):
        now = datetime.datetime.now()
        object_name = f"{now.year}/{now.month}/{now.day}/{now.hour}/profile_image_{uuid.uuid4()}.png"
        return self.create_signed_url_for_post_upload(object_name)

    @staticmethod
    def create_signed_url_for_post_upload(s3_object_name: str) -> SignedUploadUrlResponse:
        """Generate a signed URL S3 POST request to upload a file
        """
        upload_signed_url = SignedUploadUrlResponse({}, Status())
        try:
            s3_client = boto3.client('s3')
            bucket_name = f"{AWSConstants.PYAWS_CLI_IMAGE_SUBDOMAIN.value}.{AWSConstants.SSM_PARAMETER_PYAWS_CLI_DOMAIN.value}"
            conditions = [
                ["content-length-range", 0, 1048576]
            ]

            upload_response = s3_client.generate_presigned_post(bucket_name,
                                                                s3_object_name,
                                                                Fields=None,
                                                                Conditions=conditions,
                                                                ExpiresIn=60)
            upload_signed_url.upload = upload_response
            upload_signed_url.status.success = True
        except Exception as e:
            logger.exception(e)
            upload_signed_url.status.success = False
        return upload_signed_url


uploadService = UploadService()
  `
}
</script>

