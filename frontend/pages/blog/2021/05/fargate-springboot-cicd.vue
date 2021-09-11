<template>
  <b-tabs nav-class="separator-tabs ml-0 mb-5" content-class="tab-content" :no-fade="true">
    <b-tab title="AWS Fargate Spring Boot CI-CD">
      <div>
        <b-row>
          <b-card class="mb-4" no-body>
            <ResizeImageTag resizeTo=1200 src="blog/2021/05/cicd-pipeline.png"
                            class-name="responsive border-0 card-img-top mb-3" alt="Fargate CI-CD"/>
            <span
              class="badge badge-pill badge-theme-2 position-absolute badge-top-left">AWS Fargate Spring Boot CI-CD</span>
            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">AWS Fargate Spring Boot Continuous integration and deployment (CI-CD)</h3>
                <p></p>
                <p>In last few weeks I was working on AWS CodePipeline/Commit/Build products. In result, I finished a small
                  application that includes CDK CI-CD stack for Spring Boot webapp running inside Fargate cluster.</p>
                <p>It can be found on Github:</p>
                <a href="https://github.com/stokilo/aws-spring-cdk-ci-cd" rel="noopener noreferrer" target="_blank">https://github.com/stokilo/aws-spring-cdk-ci-cd</a>
                <p></p>
                <p>CDK stacks included in the infrastructure project provision CodeCommit repository, ECR repository,
                  CodePipeline, and Fargate cluster.
                  CodePipeline is executed on each git commit. It rebuilds the Docker Spring Boot application and redeploys
                  it on the ECS.</p>
                <p>Configuration details can be found on Github in the README.MD file. </p>
                <p></p>
              </div>

              <div class="mb-5">
                <h3 class="card-title">Cross-account stacks.</h3>
                <p>I've decided to use IaC tools to model my organization. I found an interesting project:</p>
                <a href="https://github.com/org-formation/org-formation-cli" rel="noopener noreferrer" target="_blank">https://github.com/org-formation/org-formation-cli</a>
                <p></p>
                <p>It is possible to dump your existing organization into a Cloudformation like file called
                  organization.yml.
                  Once it is done, you can edit it and add new accounts, change SCP, and many more.</p>
                <p>I've modeled a sample organization unit with the name 'STC'</p>
                <pre><code>Root
  -&gt; STC
    -&gt; INFRASTRUCTURE (account 111111111111)
       ---&gt; CodeCommit
       ---&gt; ECR
    -&gt; CICD (account 222222222222)
       ---&gt; CodePipeline
       ---&gt; Fargate cluster
    -&gt; WORKLOADS
      -&gt; DEV (account 333333333333)
      -&gt; PROD ...
      -&gt; TEST ...
</code></pre>

                <p></p>
                <p>INFRASTRUCTURE org unit holds single account 111111111111. I store there my CodeCommit and ECR
                  repositories. </p>
                <p>CICD org unit is for the CodePipeline stack. There I also run the Fargate cluster. CodePipeline checkout
                  source code
                  and fetch Docker images from 111111111111 account. </p>
                <p>This requires to configure cross-account stacks and appropriate permissions. CDK helps a lot in this
                  area. However, it was not easy to
                  find out how to do it properly. </p>
                <p>I've created a role that is allowed to be assumed by CICD account (222222222222) only. This role was
                  created in the CodeCommit account (111111111111)
                </p>
              </div>

              <client-only>
                <highlightjs langugage="java" :code="snippet1"/>
              </client-only>

              <p>Next, this role is imported into the CodePipeline stack (CICD account). I import it by ARN.</p>

              <client-only>
                <highlightjs langugage="java" :code="snippet2"/>
              </client-only>

              <p>The role is used by CodeCommitStage. There I need permission to checkout source code from the repository that
                belong to another account.
              </p>
              <client-only>
                <highlightjs langugage="java" :code="snippet3"/>
              </client-only>


              <div class="mb-5">
                <h3 class="card-title">SSO configuration</h3>
                <p>I configured my development machine to use SSO short term credentials.</p>
                <p>
                  This project includes a sample helper script (sso.sh) to refresh tokens and update ~/.aws/credentials
                  file. You first should run 'aws configure sso' from the command line and configure all your SSO profiles
                  under ~/.aws/config. Each profile has a name, region, auth link, and permission set associated.
                  This is enough for sso.sh to execute the AWS CLI command to refresh access keys under credentials file.
                  The browser window is open to input credentials and MFA token.
                </p>
                <p>
                  I store account configuration together with region and profile names under env.properties.
                  CDK deployment is wrapped with another shell script cdk.sh . This script is nothing more than
                  a set of helper functions to pass the correct profile name to the deployment target. Additionally,
                  it performs SSO token refresh.
                </p>
                <p>
                  I found this process quite ok and decided to migrate my organization to use SSO.
                  More technical details on how to configure SSO are included in the Github repository.
                </p>
              </div>


              <div class="mb-5">
                <h3 class="card-title">Deployment order</h3>
                <p></p>
                <p>All stacks must be deployed in order. You start with the infrastructure stack. Once this is done
                  you have CodeCommit and ECR repositories up and running.</p>
                <p>
                  The next step is manual. You push initial files to the repository including Dockerfile. Then you build
                  a base Docker image. I've decided to do this manually to keep things simple. Otherwise, I would have to
                  pull from the Docker registry using AWS IP. Such Docker pull requests are often rate-limited
                  and the CodeBuild stage fails. You can log in to the Docker with your credentials but this requires you to
                  store
                  your credentials in the SecretManager. To keep this project simple I've decided to build a base image
                  locally.
                  Then this image is inserted manually into Dockerfile. The CodeBuild is fetching images from AWS ECR only.
                </p>
                <p>
                  Once initial data is present in both repositories, you can deploy CICD stack. After this step,
                  CodePipeline is executed on each next commit.
                </p>
              </div>


              <div class="mb-5">
                <h3 class="card-title">Testing</h3>
                <p>The Fargate cluster is created under the CICD stack. It is updated with a new image every time you push into
                  CodeCommit repository. This process takes around 10 minutes. CDK provision Fargate cluster with public
                  application
                  load balancer. You can copy DNS name and test application from your side.</p>
                <p></p>
              </div>

              <div class="mb-5">
                <h3 class="card-title">Lessons learned</h3>

                <p>
                  1. AWS CDK heavy lifting
                </p>
                <p>
                  AWS CDK is doing a lot for you in the background. This can be misleading in some cases, sometimes
                  following AWS
                  documentation for resource setup is not required at all. For example, cross-account setup for CDK
                  requires attaching
                  an imported role from another account. CDK magically attached required policies and resolved CodeCommit
                  repository ARN.
                  Without that, you would end up with an unusable stack where AWS Console shows you the wrong account number in
                  the CodeCommit
                  ARN
                </p>
                <p>
                  => Bookmark AWS CDK Github, join slack, search existing tickets and ask questions
                </p>

                <p>
                  2. AWS CDK pipelines library
                </p>

                <p>
                  AWS CDK list some issues i.e. links on the Console won't work in a cross-account scenario. You should
                  be aware
                  that it is a limitation, but the stack works perfectly fine.
                </p>
                <p>
                  => Always check AWS CDK typescript documentation
                </p>

                <p>
                  3. SSO
                </p>
                <p>
                  Background token refresh on the web AWS Console is not consistently refreshed. You have to reload
                  browser tab manually.
                  Fortunately, you are not logged out.
                </p>
                <p>
                  Session duration is set to 4 hours, it is ok for regular work use cases.
                </p>
                <p>
                  => Use SSO whenever possible regardless of small issues and requirement to refresh ~/.aws/credentials
                  with sso.sh
                  script
                </p>

                <p>
                  4. Cross account browser workspace
                </p>

                <p>
                  I found the best for my use case to use the same browser with one regular window and one in private mode.
                </p>

                <p>
                  => Working with  single browser allows accessing your private bookmarks. Don't trust browser extensions
                  for manage isolated
                  sessions, this is too risky.
                </p>

                <p>
                  5. ECR repository permission
                </p>
                <p>
                  Docker introduced rate-limiting for unauthorized pull requests. This affects code pipeline workflows,
                  it is easy to
                  get rate limited on Docker pull because requests are executed from AWS network. The suggested workaround
                  is to configure Docker
                  credentials and use them to log in. This requires managing secrets. I've decided to
                  push my base images and use them for Dockerfile FROM clause. However, this resulted in a requirement to
                  add to my policy
                  ARN with /repository path (see the code).
                </p>

                <p>
                  => Keep it simple for testing stacks.
                </p>

                <p>
                  6. AWS CDK source code
                </p>

                <p>
                  Checkout AWS CDK source code. It is implemented in a typescript language. It is useful for tracing
                  more
                  complex issues.
                </p>

                <p>
                  => Check the source code before you ask the question.
                </p>
                <p></p>
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
//@ts-ignore


@Component({
  components: {
    ResizeImageTag,
    ResponsiveImageTag,
    Colxx
  },
  head: {
    title: 'AWS Fargate Spring Boot CI-CD',
    meta: [
      {
        hid: 'description',
        name: 'description',
        content: 'AWS Fargate SpringBoot CI-CD'
      },
      {
        hid: 'keywords',
        name: 'keywords',
        content: 'aws, cdk, Fargate, CI, CD, CICD, SpringBoot'
      }
    ]
  }
})
export default class AwsFargateSpringBootCICD extends Vue {

  snippet1: String = `
Role codeCommitAccessRole = new Role(this, CODE_COMMIT_ACCESS_ROLE, RoleProps.builder()
        .description("Role for accessing CodeCommit repository")
        .assumedBy(new AccountPrincipal(props.ciCdAccountId))
        .roleName(CODE_COMMIT_ACCESS_ROLE)
        .build());


codeCommitAccessRole.addToPolicy(PolicyStatement.Builder.create()
        .effect(Effect.ALLOW)
        .resources(Collections.singletonList(codeCommitRepository.getRepositoryArn()))
        .actions(Arrays.asList(
                "codecommit:GitPull",
                "codecommit:GetBranch",
                "codecommit:GetCommit",
                "codecommit:ListBranches",
                "codecommit:GetUploadArchiveStatus",
                "codecommit:ListRepositories",
                "codecommit:UploadArchive",
                "codecommit:GetCommitHistory"
                ))
        .build());

        codeCommitAccessRole.addToPolicy(PolicyStatement.Builder.create()
        .effect(Effect.ALLOW)
        .resources(Arrays.asList(
                "arn:aws:s3:::codepipeline-*",
                "arn:aws:s3:::codepipeline-*/*",
                String.format("arn:aws:kms:%s:%s:key/*", props.region, props.ciCdAccountId)
        ))
        .actions(Arrays.asList(
                "s3:GetObject*",
                "s3:GetBucket*",
                "s3:List*",
                "s3:DeleteObject*",
                "s3:PutObject*",
                "s3:Abort*",
                "kms:Decrypt",
                "kms:DescribeKey",
                "kms:Encrypt",
                "kms:ReEncrypt*",
                "kms:GenerateDataKey*"
        ))
        .build());
  `

  snippet2: String = `
IRole infrastructureAccessRole = Role.fromRoleArn(this, "infrastructureAccessRole",
        String.format("arn:aws:iam::%s:role/%s",
                props.infrastructureAccountId, CodeCommitStack.CODE_COMMIT_ACCESS_ROLE));
  `

  snippet3: String = `
StageProps.builder()
    .stageName("CodeCommitStage")
    .actions(Collections.singletonList(
            CodeCommitSourceAction.Builder.create()
                    .actionName("CodeCommitSource")
                    .repository(codeCommitRepo)
                    .output(sourceOutput)
                    .branch("master")
                    .role(infrastructureAccessRole)
                    .trigger(CodeCommitTrigger.POLL)
                    .build()
    ))
    .build(),
  `
}

</script>
