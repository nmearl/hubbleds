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
      <strong>There is no right answer</strong>, but we hope this story has given you a better understanding of how scientists use data to determine how much confidence you can have in a new result.
    </p>
    <p>
      Science is always moving forward and there is always more humans can learn about our universe. Follow NASA to learn what new discoveries are being made by HST's successor, the James Webb Space Telescope!
    </p>
  </div>
  </scaffold-alert>
</template>

<script setup>
</script>
