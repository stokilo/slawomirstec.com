import {createModule, mutation, action} from "vuex-class-component";
import {ContactModelSubmitResult, Contact} from "~/store/model/profile/contact";
import ContactService from "~/store/api/profile/contact-service";

export const VuexModule = createModule({
  namespaced: "contact",
  strict: false,
  target: "nuxt",
});

export class ContactStore extends VuexModule {

  contact: Contact = new Contact();

  contactService: ContactService = new ContactService();

  @mutation mutateContact(mutatedContact: Contact) {
    this.contact = mutatedContact;
  }

  @mutation mutateContactReCaptcha(token: string) {
    this.contact.recaptcha.token = token
  }

  @action
  async onMounted() {
    if (process.env.isDevMode) {
      let contactInitData = new Contact();
      contactInitData.name = "John Doe";
      contactInitData.email = "test@test.com";
      contactInitData.details = "Test message"
      this.mutateContact(
        contactInitData
      )
    }
  }

  @action
  async onSaveContact() : Promise<ContactModelSubmitResult> {
    return await this.contactService.saveContact(this.contact)
  }


}

