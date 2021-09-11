<template>
  <div>
    <AppointmentCalendar :editable="true"/>
  </div>
</template>

<script>
import AppointmentCalendar from "@/components/app/appointment/AppointmentCalendar";

export default {
  layout: "app-layout",
  components: {
    AppointmentCalendar
  }
}
</script>
