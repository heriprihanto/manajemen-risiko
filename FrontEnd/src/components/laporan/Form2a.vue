<script setup>
defineProps({ data: { type: Object, default: null }, tahun: [Number, String] })
</script>

<template>
  <section class="report-section">
    <div class="report-formno">Form 2.a</div>
    <div class="report-title">Penetapan Konteks Risiko Strategis Pemda</div>
    <div class="report-subtitle">Tahun {{ tahun }}</div>
    <table class="rpt">
      <tbody v-if="data">
        <tr><th style="width: 280px; text-align: left">Visi</th><td>{{ data.visi }}</td></tr>
        <tr><th style="text-align: left">Misi Strategis</th><td>{{ data.misi_strategis }}</td></tr>
        <tr><th style="text-align: left">Tujuan Strategis RPD</th><td>{{ data.tujuan_strategis }}</td></tr>
        <tr><th style="text-align: left">Penetapan Konteks Tujuan</th><td>{{ data.penetapan_konteks_tujuan }}</td></tr>
        <tr><th style="text-align: left">Sasaran RPD</th><td>{{ data.sasaran_rpd }}</td></tr>
        <tr><th style="text-align: left">Penetapan Konteks Sasaran</th><td>{{ data.penetapan_konteks_sasaran }}</td></tr>
        <tr><th style="text-align: left">IKU Sasaran</th><td>{{ data.iku_sasaran }}</td></tr>
        <tr><th style="text-align: left">Urusan Pemerintahan</th><td>{{ data.urusan_pemerintahan }}</td></tr>
      </tbody>
      <tbody v-else><tr><td class="c">Belum ada data</td></tr></tbody>
    </table>
  </section>
</template>
