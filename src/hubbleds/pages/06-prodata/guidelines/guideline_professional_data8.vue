<!-- # multiple choice -->
<template>
  <scaffold-alert
    color="info"
    class="mb-4 mx-auto"
    max-width="800"
    elevation="6"
    @back="back_callback()"
    @next="next_callback()"
    :can-advance="can_advance"
  >
    <div
      class="mb-4"
    >
      Reflect a bit on what this tells you.
      <v-container
        class="px-0"
        fluid
      >
      
      <p> What did astronomers in the early 1920's believe about the universe before Edwin Hubble's discovery?</p>
      <free-response
        outlined
        auto-grow
        rows="2"
        label="Reflection #1"
        tag="prodata-reflect-8a"
      ></free-response>
      
      <p>What age of the universe can be obtained from Edwin Hubble's data (in Gyr)?</p>
      <free-response
        outlined
        auto-grow
        rows="2"
        label="Age from Edwin Hubble"
        tag="prodata-reflect-8b"
        type="float"
      ></free-response>
      
    <p>What age of the universe can be obtained from the HST Key project's data (in Gyr)?</p>
      <free-response
        outlined
        auto-grow
        rows="2"
        label="Age from HST Key Project"
        tag="prodata-reflect-8c"
        type="float"
      ></free-response>
      </v-container>
    </div>
  </scaffold-alert>
</template>

<script setup>

</script>
