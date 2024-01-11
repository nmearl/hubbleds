<template>
  <scaffold-alert
    title-text="Class Age Range"
    @back="state.marker_backward = 1"
    @next="state.marker_forward = 1"
  >
    <div
      class="mb-4"
      v-intersect="checkIntersecting"
    >
      <v-card
        class="JaxEquation pa-3"
        color="info lighten-1"
        elevation="0"
      >        
        $$ \text{Low age: } \textcolor{black}{\colorbox{#FFAB91}{ {{ (state.stu_low_age).toFixed(0) }} } } \text{ Gyr} $$
        $$ \text{High age: } \textcolor{black}{\colorbox{#FFAB91}{ {{ (state.stu_high_age).toFixed(0) }} } } \text{ Gyr} $$
      </v-card>
      <p class="mt-4">
        Also, the universe’s age could have been anywhere from thousands of years to trillions or more years. The fact that everyone in your class got an age within 10’s of billions of years of each other is actually pretty well constrained.
      </p>
    </div>
  </scaffold-alert>
</template>

<style>
  .JaxEquation .MathJax {
    margin: 3px auto !important;
  }
</style>

<script>
module.exports = {
  props: ['state'],
  computed: {
    checkIntersecting(entries, _observer, intersecting) { if (intersecting) { window.MathJax.typesetPromise(entries.map(entry => entry.target)) }}
  }
}
</script>
