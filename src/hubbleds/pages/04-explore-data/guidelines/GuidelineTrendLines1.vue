<template>
  <scaffold-alert
    title-text="Trend Lines"
    @back="back_callback()"
    @next="next_callback()"
    :can-advance="can_advance"
  >
    <div
      class="mb-4"
    >
      <p>
        Let's return to your own 5 data points and see what we can learn from them now that we are aware of a trend in the larger data set.
      </p>
    </div>
  </scaffold-alert>
</template>
