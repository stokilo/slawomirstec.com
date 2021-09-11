<template>
  <b-tabs nav-class="separator-tabs ml-0 mb-5" content-class="tab-content" :no-fade="true">
    <b-tab title="AWS CDK Java setup for RDS and Vpn Client">
      <div>
        <b-row>
          <b-card class="mb-4" no-body>
            <ResizeImageTag resizeTo=1200 src="blog/2021/04/rds-vpn.png"
                            class-name="responsive border-0 card-img-top mb-3" alt="CDK RDS VPN"/>
            <span
              class="badge badge-pill badge-theme-2 position-absolute badge-top-left">AWS CDK RDS + VPN</span>
            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">AWS CDK Java setup for Aurora RDS and Client VPN</h3>
                <p></p>
                <p>
                This is a documentation post for a sample Java AWS CDK setup that I've created while preparing
                for a certification exam. I've created a CDK stack with the following elements:
                </p>
                <ul class="list-unstyled">
                  <li>1. VPC setup with two private subnets and one public</li>
                  <li>2. RDS Aurora with the single master node, deployed in two AZ</li>
                  <li>3. Client VPN setup</li>
                  <li>4. Route53 private and public hosted zone configuration</li>
                </ul>
                <p>
                  It is only for presentation purpose, it is hosted on Github:
                </p>
                <a href="https://github.com/stokilo/aws-cdk-rds-vpn" rel="noopener noreferrer" target="_blank">https://github.com/stokilo/aws-cdk-rds-vpn</a>
                <p></p>
                <p>
                  I want to document what I wanted to achieve and all my findings during development.
                </p>
                <p>
                </p>
              </div>

              <div class="mb-5">
                <h3 class="card-title">Setup</h3>
                <p></p>
                <p>
                  Original idea was to create a new, non-default VPC with two 3 subnets. First two as
                  private and the third one as public. The CDK automatically configure a NAT Gateway when a private
                  subnet is defined. In my case, I didn't want to pay for that and I don't need outgoing connections.
                  By selecting <b>isolated</b> subnet type Nat Gateway is not created. This is what I needed for RDS
                  setup.
                </p>
                <p>
                  In the private subnet, I deployed Aurora Postgres database. It was configured in a single master mode and
                  deployed in 2 AZ for HA. I wanted to connect to reader and writer endpoints using the fixed name.
                  I've decided to call them reader.rds.com and writer.rds.com. This allows me to configure the database
                  client and save connections in it without the need to reconfigure it every time stack are redeployed.
                </p>
                <p></p>
                <p>Additionally, I wanted to connect directly to the database hosted on AWS instances.
                  Of course, it would be much cheaper setup it on my local machine i.e. in docker container.
                  This is not what I wanted. In the future, I plan to rewrite this stack and setup Aurora serverless with the Data Api.

                  I've decided to use VPN client connection and connect to the VPC subnet directly.
                  There is a product in AWS called VpnClient. That is what I provision in the sample project because it is good for a solo dev setup.
                </p>
                <p>
                  I own a domain awss.ws, I wanted to have a subdomain vpn.awss.ws and always connect to this address with OpenVpn client.
                  AWS VpnClient generates endpoint URL and every time stack is deployed, a new name is assigned.
                  Adding this to Route53 manually is cumbersome process. That is why my stack setup public hosted zone
                  CNAME entries to allow me hardcode vpn.awss.ws in my OpenVpn config file.
                </p>
                <p></p>
                <p></p>
              </div>

              <div class="mb-5">
                <h3 class="card-title">Java CDK</h3>
                <p></p>
                <p>
                  My slawomirstec.com website is provisioned with CDK using Python language. Here I decided to use Java.
                  CDK and lambda code that is required for some post-deployment steps, are contained in separated maven modules.
                  I build both from the parent module, I had to use custom app launcher code in cdk.json.
                </p>
                <p></p>
                <client-only>
                  <highlightjs langugage="python" :code="snippet1"/>
                </client-only>
                <p></p>
                <p>CDK code is in the module cdk, main class of course too.</p>
                <p>I could not find BOM for CDK, it was only available for SDK</p>
                <p></p>
              </div>


              <div class="mb-5">
                <h3 class="card-title">Runner script</h3>
                <p></p>
                <p>The cdk application is wrapped into custom cdk.sh script. This script allows to define a target deployment account using
                env.properties file. There I configure account/region/public hosted zone/domain name
                settings per environment. I don't like AWS CLI and CDK profile discovery logic, I use separate accounts
                per stage system, it is possible to deploy by accident dev stack to prod. I added some code to
                cross-check profile discovered from AWS credentials and match it with the configured account in env.properties.</p>
                <p></p>
                <client-only>
                  <highlightjs langugage="python" :code="snippet2"/>
                </client-only>
                <p></p>
              </div>

              <div class="mb-5">
                <h3 class="card-title">VPC setup</h3>
                <p></p>
                <p>AWS CDK provides default values for services, I find out that you can get NAT gateway automatically
                configured depending on the selected subnet type. VPC has two subnets that are isolated from the public
                internet. These are for RDS deployment and the VpnClient association. Security group only allows Postgres and
                DNS ingress traffic. DNS is set to default reserved VPC DNS IP, not to the host DNS where OpenVpn is running.
                This is required to resolve private hosted zone names (*.rds.com).</p>
                <p></p>
                <p>*VPC default DNS is not always working, this is still todo on my list to inspect real cause.
                It is possible that I have major configuration issue in the CDK code.</p>
                <p></p>
              </div>

              <div class="mb-5">
                <h3 class="card-title">VpnClient</h3>
                <p></p>
                <p>VpnClient configuration was easy, sample code below for PROD and DEV.
                   The latest CDK version handles a lot of details for you in the background. No need to
                   define Vpn connection associations, security groups, or authorization. All is resolved by the
                   library on synth time.
                  </p>
                <client-only>
                  <highlightjs langugage="python" :code="snippet3"/>
                </client-only>
                <p>
                  More work was required to update the CNAME record in a public DNS zone.
                  I could not find the way hot to get back autogenerated DNS name for the Vpn endpoint.
                  AWS SDK has a method 'describeClientVpnEndpoints' that can return a list of all endpoints.
                  But here is a problem. CDK is provisioning infrastructure and there is no easy way to instruct
                  it to do some extra work outside provided API. And it should not be done like that because
                  the CDK code should be responsible for all infrastructure elements to safely update or destroy it.
                  </p><p>
                  Running custom logic after stack deployment can lead to unmaintainable stack.
                  But here I didn't have a choice, API is not allowing me to extract DNS name from the
                  Vpn endpoint. Additionally, I've updated the existing, public-hosted zone in Route53. I don't provision this
                  part of infrastructure with CDK. That is why I assume this is safe to add one record after the main
                  stack is deployed.

                  In order to execute post-processing logic after deployment, I've implemented a step function workflow
                  that calls a lambda function every minute until the stack is up. The step function is triggered by the EventBridge
                  rule 5 minutes after deployment. This is of course in theory, in practice, part of the stack with
                  the rule is executed first, before VPC/Vpn Client is deployed. However, lambda code handles failure
                  and step function executes it until success is returned from. Sample code below.


                <p></p>
                <client-only>
                  <highlightjs langugage="python" :code="snippet3"/>
                </client-only>
                <p>I did a big mistake and deployed an infinite loop in the step function :)</p>
                <p>I've received an email from AWS about the end of my free tier for step functions.
                I was surprised because I have one wait condition, one lambda step, and a choice element.
                Of course, I didn't connect Choice with wait condition but directly to lambda, which caused
                an infinite loop until the whole stack was deployed. I was lucky that there was a timeout set for
                step function to 1 hour and lambda returned success pretty quickly after deployment</p>
                <p></p>
                <p>Another important lesson from working with the CDK. Don't update or delete anything that was created
                by the CDK. This will cause the failure of the CDK update in the future. Even small changes prevent you from
                updating the stack or even destroying it.</p>
                <p>I found that deploying an isolated stack works the best. In case anything fails, I destroy the stack
                and recreate it again.</p>
                <p>Additionally, I've noticed that sometimes my DNS resolution is not working after connecting to
                the VPN. I'm using VPC internal DNS for resolving IP addresses. I don't use my host DNS server because
                I want to resolve private hosted zone RDS names. It is a random error, something is wrong with the stack
                I've created or the region I operate in (Bahrain). </p>
                <p></p>
                <client-only>
                  <highlightjs langugage="python" :code="snippet4"/>
                </client-only>
              </div>

              <div class="mb-5">
                <h3 class="card-title">Final words</h3>
                <p></p>
                <p>Github repo contains README on how to do all setup steps required to bring the services up.
                  There is no need to repeat it here. I plan to evolve this stack and replace RDS with Aurora serveless
                  and Data API. For backend services, I will add integration with Fargate and sample spring boot application.
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
    title: 'AWS CDK Aurora and Client Vpn setup',
    meta: [
      {
        hid: 'description',
        name: 'description',
        content: 'AWS CDK RDS Clien Vpn setup'
      },
      {
        hid: 'keywords',
        name: 'keywords',
        content: 'aws, cdk, rds, ClientVpn, vpn, aurora'
      }
    ]
  }
})
export default class AwsCdkRdsVpn extends Vue {

  snippet1: String = `
    "app": "mvn package && mvn -e -q exec:java -pl cdk -Dexec.mainClass=com.sstec.cdk.rdsvpn.RdsVpnApp"
  `
  snippet2: String = `
#dev
dev.account=
dev.region=
dev.hosted.zone.id=
dev.vpn.host.url=

#production
prod.account=
prod.region=
prod.hosted.zone.id=
prod.vpn.host.url=
  `

  snippet3: String = `
  public class VpnClientStack extends Stack {

    public static final String CLIENT_CIDR = "10.16.0.0/22";
    public static final String TRAINING_CLIENT_VPN_ENDPOINT = "trainingClientVpnEndpoint";

    public VpnClientStack(final Construct scope, final String id, final MultiStageStackProps props) {
        super(scope, id, props.props);

        String clientCertToken = StringParameter.valueForStringParameter(
                this, "client-cert-parameter");
        String serverCertToken = StringParameter.valueForStringParameter(
                this, "server-cert-parameter");

        if (props.isProd) {
            // HA, AWS charges for each of the subnet association, our VPS has 2 isolated subnets, it cost 2x for standby
            props.clientVpnEndpoint = new ClientVpnEndpoint(this, VpnClientStack.TRAINING_CLIENT_VPN_ENDPOINT,
                    ClientVpnEndpointProps.builder()
                            .clientCertificateArn(clientCertToken)
                            .serverCertificateArn(serverCertToken)
                            .vpc(props.vpc)
                            .splitTunnel(true)
                            .selfServicePortal(false)
                            .vpcSubnets(SubnetSelection.builder().onePerAz(true).subnetType(SubnetType.ISOLATED).build())
                            .cidr(VpnClientStack.CLIENT_CIDR)
                            .build());

        } else if (props.isDev) {
            props.clientVpnEndpoint = new ClientVpnEndpoint(this, VpnClientStack.TRAINING_CLIENT_VPN_ENDPOINT,
                    ClientVpnEndpointProps.builder()
                            .clientCertificateArn(clientCertToken)
                            .serverCertificateArn(serverCertToken)
                            .vpc(props.vpc)
                            .splitTunnel(true)
                            .logging(false)
                            .selfServicePortal(false)
                            .dnsServers(Collections.singletonList(VPCStack.VPC_DNS))
                            .securityGroups(Collections.singletonList(props.vpnRdsSecurityGroup))
                            .vpcSubnets(SubnetSelection.builder()
                                    .availabilityZones(props.vpc.getAvailabilityZones().subList(1, 2))
                                    .subnetGroupName(VPCStack.SUBNET_DB_NAME)
                                    .build())
                            .cidr(VpnClientStack.CLIENT_CIDR)
                            .build());
        }
        Tagging.addEnvironmentTag(props.clientVpnEndpoint, props);
    }
}

  `

  snippet4: String = `
package com.sstec.cdk.rdsvpn.stacks;

import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.Collections;
import java.util.HashMap;
import java.util.UUID;

import com.sstec.cdk.rdsvpn.MultiStageStackProps;
import com.sstec.cdk.rdsvpn.Tagging;
import software.amazon.awscdk.core.Construct;
import software.amazon.awscdk.core.Duration;
import software.amazon.awscdk.core.RemovalPolicy;
import software.amazon.awscdk.core.Stack;
import software.amazon.awscdk.services.events.*;
import software.amazon.awscdk.services.events.targets.SfnStateMachine;
import software.amazon.awscdk.services.iam.Effect;
import software.amazon.awscdk.services.iam.PolicyStatement;
import software.amazon.awscdk.services.lambda.Code;
import software.amazon.awscdk.services.lambda.Runtime;
import software.amazon.awscdk.services.lambda.SingletonFunction;
import software.amazon.awscdk.services.logs.LogGroup;
import software.amazon.awscdk.services.logs.RetentionDays;
import software.amazon.awscdk.services.stepfunctions.*;
import software.amazon.awscdk.services.stepfunctions.tasks.LambdaInvoke;


/**
 * CDK PostDeploy lambda.
 */
public class PostDeployStack extends Stack {
    public PostDeployStack(final Construct parent, final String name, final MultiStageStackProps props) {
        super(parent, name, props.props);

        SingletonFunction lambdaFunction =
                SingletonFunction.Builder.create(this, "cdk-post-deploy-lambda")
                        .description("CDK Post deploy lambda")
                        .environment(new HashMap<String, String>() {{
                            put("HOSTED_ZONE_ID", props.hostedZoneId);
                            put("VPN_HOST_URL", props.vpnHostUrl);
                        }})
                        .code(Code.fromAsset("./lambda/out/rds-vpn-lambda.jar"))
                        .handler("com.sstec.cdk.rdsvpn.PostDeploy")
                        .logRetention(RetentionDays.ONE_DAY)
                        .timeout(Duration.seconds(15))
                        .memorySize(512)
                        .runtime(Runtime.JAVA_8)
                        .uuid(UUID.randomUUID().toString())
                        .build();
        Tagging.addEnvironmentTag(lambdaFunction, props);

        lambdaFunction.addToRolePolicy(PolicyStatement.Builder.create()
                .effect(Effect.ALLOW)
                .actions(Collections.singletonList("ec2:DescribeClientVpnEndpoints"))
                .resources(Collections.singletonList("*"))
                .build());

        lambdaFunction.addToRolePolicy(PolicyStatement.Builder.create()
                .effect(Effect.ALLOW)
                .actions(Collections.singletonList("route53:ChangeResourceRecordSets"))
                .resources(Collections.singletonList(String.format("arn:aws:route53:::hostedzone/%s", props.hostedZoneId)))
                .build());

        LambdaInvoke taskLambda = LambdaInvoke.Builder.create(this, "lambdaInvokeStep")
                .lambdaFunction(lambdaFunction)
                .build();

        Wait waitOneMinute = Wait.Builder.create(this, "waitCondition").time(
                WaitTime.duration(Duration.minutes(1))).build();

        Fail fail = Fail.Builder.create(this, "fail").error("This is final step").build();
        Pass pass = Pass.Builder.create(this, "pass").build();

        Chain steps = waitOneMinute
                .next(taskLambda)
                .next(Choice.Builder.create(this, "Choice")
                        .build()
                        .when(Condition.stringEquals("$.Payload", "SUCCESS"), pass)
                        .when(Condition.stringEquals("$.Payload", "FAILED"), waitOneMinute)
                        .otherwise(waitOneMinute)
                );

        StateMachine stateMachine = StateMachine.Builder
                .create(this, "cdkPostDeployStateMachine")
                .stateMachineName("CdkPostDeployStateMachine")
                .logs(LogOptions.builder().includeExecutionData(true).destination(
                        LogGroup.Builder.create(this, "stepFunctionGroup")
                                .removalPolicy(RemovalPolicy.DESTROY)
                                .retention(RetentionDays.ONE_DAY)
                                .logGroupName("PostDeployStepFunction").build()).build())
                .stateMachineType(StateMachineType.STANDARD)
                .definition(steps)
                .timeout(Duration.hours(1))
                .build();
        Tagging.addEnvironmentTag(stateMachine, props);


        // trigger state machine execution 5 minutes from now, state machine will attempt to update public
        // hosted zone CNAME entry for VPN Connection endpoint
        LocalDateTime nowPlus5 = LocalDateTime.now(ZoneOffset.UTC).plusMinutes(5);
        Schedule inNext5Min = Schedule.cron(CronOptions.builder()
                .day(String.valueOf(nowPlus5.getDayOfMonth()))
                .month(String.valueOf(nowPlus5.getMonth().getValue()))
                .year(String.valueOf(nowPlus5.getYear()))
                .hour(String.valueOf(nowPlus5.getHour()))
                .minute(String.valueOf(nowPlus5.getMinute())).build());

        Rule.Builder.create(this, "startCdkPostDeployStateMachine5MinAfterDeployment")
                .ruleName("run-state-machine-5min-after-deployment")
                .targets(Collections.singletonList(SfnStateMachine.Builder.create(stateMachine).build()))
                .schedule(inNext5Min)
                .build();
    }
}
  `
}
</script>

