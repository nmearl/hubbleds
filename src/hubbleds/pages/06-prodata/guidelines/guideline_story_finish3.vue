<template>
  <scaffold-alert
  @back="back_callback()"
  @next="next_callback()"
  :can-advance="can_advance"
  >
    <div
      class="mb-4"
    >
    <p>
      Thank you so much for pilot testing the Hubble Data Story. Please complete this final survey.
    </p>
            <v-btn
              block
              class="black--text"
              color="accent"
              elevation="2"
              target="_blank"
              href='https://harvard.az1.qualtrics.com/jfe/form/SV_d0V9oiJpW0jjz94'
            >
              <strong>survey</strong>
            </v-btn>
    </div>
  </scaffold-alert>
</template>

<script setup>
</script>
