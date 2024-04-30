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
        Now let's consider more modern data from 2001, shown in lime green. 
      </p>
      <p>
        This data is from the HST Key Project, led by astronomer Wendy Freedman, who used data from the Hubble Space Telescope to measure a quantity known as the <strong>Hubble constant</strong>
        (which is the inverse of the age value you calculated).
      </p>
    </div>
  </scaffold-alert>
</template>

<script setup>

</script>
