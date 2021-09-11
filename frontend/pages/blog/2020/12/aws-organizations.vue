<template>
  <b-tabs nav-class="separator-tabs ml-0 mb-5" content-class="tab-content" :no-fade="true">
    <b-tab title="AWS organizations">
      <div>
        <b-row>
          <b-card class="mb-4" no-body>
            <ResizeImageTag resizeTo=1200 src="blog/2020/12/org-1.jpg"
                            class-name="responsive border-0 card-img-top mb-3" alt="Organization accounts"/>
            <span
              class="badge badge-pill badge-theme-2 position-absolute badge-top-left">AWS organization</span>
            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">AWS Organizations</h3>
                <p>
                  AWS organization is a service for central management of the accounts, environments and resources.
                  I decided to give it a try and configure it for my website.
                </p>
                <p></p>
                <p>
                  My requirements were simple, I needed dev and production environments, both fully separated from
                  each other. Google gives few ideas on how to solve this problem, I divided them into two groups:
                </p>
                <ol class="list-group">
                  <li>
                    Single account approach. Separation of the services is the responsibility of the developers.
                    Various techniques must be employed to do it correctly.
                  </li>
                  <li>
                    Multi-account approach. One account for each stage system. By account, I mean root account with an associated
                    payment method. Services are naturally separated with the option to consolidate the bill from all accounts.
                  </li>
                </ol>
                <p></p>
                <p>
                   I decided to create my organization and try a multi-account approach.
                   'Aws organization' image is a screenshot of the organization I created (with faked private data).
                   I created following accounts:
                </p>
                <ol class="list-group">
                  <li>Root account for consolidated billing. It is a management account (root@email.com)</li>
                  <li>Production account (prod@email.com)</li>
                  <li>Development account (dev@email.com)</li>
                </ol>
                <p></p>
                <p>
                  Accounts were assigned to the organization tree like below:
                </p>
                <ResizeImageTag resizeTo=1200 src="blog/2020/12/org-tree.jpg"
                                class-name="responsive border-0 card-img-top mb-3" alt="Organization tree"/>
                <p></p>
                <p>
                  And that is all I did with organization setup. Rest of the setup is an account setup
                  that has nothing to do with the organization. Organization setup resulted in consolidated billing setup,
                  in the bill overview all accounts were listed automatically after few hours. I haven't tested organization
                  service control policies (SCP).
                  Firstly, there are some negative opinion about complexity of debugging of the applications with SCP
                  enabled. Secondly, sample application is too small to try it out. However, I will try organization
                  backup policies soon and write about it.
                </p>
                <p></p>
                <p></p>
              </div>
              <hr/>

              <div class="mb-5">
                <h3 class="card-title">Secret management</h3>
                <p>
                  Ok, we have 3 new accounts. Root account for billing, dev and prod accounts for deployments.
                  Additionally, I have created one admin user per deployment account (dev and prod). Admin account gets assigned groups
                  with rights only to services that are required by application to run. Admin accounts are created for security reason,
                  dev-prod deployment accounts are at same time the root accounts. All services are available there,
                  admin account is created with subset of rights to limit impact radius in case of account takeover.
                  Admin users gets programmatic access rights (access token key and secret), other accounts can only login via AWS Console.
                </p>
                <p></p>
                <p>
                  Lets list all secrets that must be maintained for this setup
                </p>
                <p></p>
                <ol class="list-group">
                  <li>3 root accounts - credentials for email accounts</li>
                  <li>3 root accounts - credentials for AWS root accounts</li>
                  <li>2 admin accounts - credentials for AWS user accounts</li>
                  <li>2 account numbers for dev and production</li>
                  <li>1 account number for management account</li>
                </ol>
                <p></p>
                <p>
                  This is a lot for such a simple setup and includes only AWS accounts.
                  I decided for following strategy to keep secrets safe.
                </p>
                <p>
                All passwords are stored in the macOS KeyChain application. KeyChain cloud backup is enabled.
                Additional backup is performed with weekly macOS backup job.
                Passwords are generated using KeyChain and are a minimum of 30 characters long.
                </p>
                <p></p>
                <p>
                  All accounts have enabled software multi-factor authentication (MFA).
                  I am using the iOS Authy application. Application backup account MFA setup to the cloud.
                  I use a PIN to secure access to the Authy on my phone + Face ID phone lock + Find My iPhone is enabled.
                </p>
                <p>Additionally, account setup configuration is included in the document package of the project.
                </p>
                <p></p>
                <p>
                  The next step was a setup of user groups for admin accounts. I enabled only DynamoDb, Lambda, CloudWatch,
                  SNS, ApiGateway services there. I did also email verification to be able to send administration emails.
                  I could not automate these steps, I will try fix it in the future.
                </p>
                <p>
                  I've additionally enabled SMS notifications for consolidated billing. I should receive a message
                  in three cases when the budget limit is reached. It was required to set up SNS Topic and Subscription and
                  connect it with all budget items. I faced an issue with the error message that Topic ARN was incorrect,
                  I fixed it by creating a topic in the default region of the root user.
                </p>
                <p>
                  An AWS Budget is not the only place where I monitor the spending. I configured a scheduled job to run lambda
                  and send a notification to the admin when a high load is detected. This is combined with rate limiting for
                  ApiGateway and low RCU/WCU set for DynamoDb. I keep it low for sample application to avoid higher
                  bills. Consolidate billing setup with organization makes it much easier.
                </p>
              </div>
              <hr/>
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
    title: 'AWS organization setup for PyAws sample application',
    meta: [
      {hid: 'description', name: 'description', content: 'Description of AWS accounts that belong to organization'},
      {
        hid: 'keywords',
        name: 'keywords',
        content: 'AWS, Organizations, backend, secrets, account, management, provisioning'
      }
    ]
  }
})
export default class AwsOrganizations extends Vue {
  snippet1: String = `

   `
}
</script>

