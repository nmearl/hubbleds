<template>
  <scaffold-alert
    title-text="Velocity Calculation"
    @back="state.marker_backward = 1"
    @next="state.marker_forward = 1"
  >
    <div
      class="mb-4"
    >
      <p>
        Now, you will use the observed wavelength of the H-&alpha; spectral line to determine the galaxy's velocity, using the <strong>Doppler Equation</strong>.

      </p>
    </div>
  </scaffold-alert>
</template>

<script>
module.exports = {
  props: ['state'],
  // mounted() {
  //   let mathJaxScript = document.createElement('script')
  //   mathJaxScript.setAttribute('src', 'https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS-MML_CHTML')
  //   document.head.appendChild(mathJaxScript)
  // },
}
</script>
