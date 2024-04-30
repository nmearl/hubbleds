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
      Nice work! You have completed the Hubble Data Story and determined an age for our universe. Check out your total <v-icon>mdi-piggy-bank</v-icon> points in the upper right of the screen.
    </p>
    <p>
      Now you may be wondering "So what's the <strong>right</strong> answer?"
    </p>
  </div>
  </scaffold-alert>
</template>

<script setup>
</script>
