<!-- this state.marker = 'lac_bia2' -->
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
        Again, assuming no systematic bias, let’s consider two scenarios:
      </p>
      <p>
        If a <strong>student</strong> only makes one measurement, what do you think are the chances their measured value will be within 2-3 Gyr of the actual age of the universe?
      </p>
      <free-response
        outlined
        auto-grow
        rows=2
        label="What are the chances"
        tag="student-chances"
        hint="Estimate how many measurement counts are within 2-3 Gyr of the central value and divide by the total number of measurements."
      ></free-response>
    </div>
    <div
      class="mb-4"
    >
      <p>
        If a <strong>class</strong> only makes one measurement, what do you think are the chances their measured value will be within 2-3 Gyr of the actual age of the universe?
      </p>
      <free-response
        outlined
        auto-grow
        rows=2
        label="What are the chances"
        tag="class-chances"
        hint="Estimate how many measurement counts are within 2-3 Gyr of the central value and divide by the total number of measurements."
      ></free-response>
    </div>
  </scaffold-alert>
</template>

<script>
module.exports = {
  props: ['state']
}
</script>
