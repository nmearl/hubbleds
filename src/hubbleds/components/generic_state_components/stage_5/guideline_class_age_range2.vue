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
        At first glance, this may seem like a large spread in possible age values for the universe. But if you think back to what astronomers knew in the 1920’s, the common scientific view was that the universe has always existed. So being able to measure any finite age for the universe was a BIG DEAL. 
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
