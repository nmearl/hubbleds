<!-- this state.marker = 'lac_bia3' -->
<template>
  <scaffold-alert
    title-text="Which Might Produce a Closer Result?"
    @back="state.marker_backward = 1"
    @next="state.marker_forward = 1"
  >
    <div
      class="mb-4"
    >
      <p>
        Why do you think the class (with 50-100 galaxies) is likely to produce a result closer to the true value than a student (with 5 galaxies)?
      </p>
      <free-response
        outlined
        auto-grow
        rows=2
        label="Reason"
        tag="reason-class-closer"
      ></free-response>
    </div>
  </scaffold-alert>
</template>

<script>
module.exports = {
  props: ['state']
}
</script>
