import {WithFromJson} from "~/store/model/shared";


export class TestAuth extends WithFromJson{
  public status: string

  constructor(status: string){
    super()
    this.status = status
  }

}


