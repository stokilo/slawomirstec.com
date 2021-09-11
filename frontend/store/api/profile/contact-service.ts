import {SERVER_API_ROUTES} from "~/store/api/routes";
import AxiosService from "~/store/api/axios-service";
import {ContactModelSubmitResult, Contact} from "~/store/model/profile/contact";
import {FormValidation, Status} from "~/store/model/shared";

export default class ContactService extends AxiosService{

  async saveContact(contact: Contact) : Promise<ContactModelSubmitResult> {
    return super.genericPost(SERVER_API_ROUTES.ROUTE_CONTACT, contact, new ContactModelSubmitResult(
      new Contact(), new Status(), new FormValidation()
    ))
  }

}
