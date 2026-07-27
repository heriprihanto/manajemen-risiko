<script setup>
defineProps({ data: { type: Array, default: () => [] }, opdName: String, tahun: [Number, String] })
</script>

<template>
  <section class="report-section">
    <div class="report-formno">Form 10</div>
    <div class="report-title">Pencatatan Kejadian Risiko (Risk Event) & Pelaksanaan RTP</div>
    <div class="report-subtitle">{{ opdName }} — Tahun {{ tahun }}</div>
    <table class="rpt">
      <thead><tr><th style="width: 90px">Kode</th><th>Risiko</th><th style="width: 80px">Tanggal</th><th>Sebab</th><th>Dampak</th><th>RTP</th><th>Realisasi RTP</th></tr></thead>
      <tbody>
        <template v-for="r in data" :key="r.risiko_id">
          <template v-for="ev in r.events" :key="ev.id">
            <tr>
              <td>{{ r.kode_risiko }}</td><td>{{ r.uraian_risiko }}</td><td class="c">{{ ev.tanggal_terjadi }}</td>
              <td>{{ ev.sebab_kejadian }}</td><td>{{ ev.dampak_kejadian }}</td><td>{{ ev.rtp }}</td><td>{{ ev.realisasi_pelaksanaan_rtp }}</td>
            </tr>
          </template>
        </template>
        <tr v-if="!data.some((r) => r.events.length)"><td colspan="7" class="c">Belum ada kejadian dicatat</td></tr>
      </tbody>
    </table>
    <div class="report-sign">
      <div class="box">
        Kota Tegal, {{ tahun }}<br />Kepala {{ opdName }}<br /><br /><br /><br />
        (...........................................)
      </div>
    </div>
  </section>
</template>
