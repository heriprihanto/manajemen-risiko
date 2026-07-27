<script setup>
import { jenisLabel } from './constants'
defineProps({ data: { type: Array, default: () => [] }, opdName: String, tahun: [Number, String] })
</script>

<template>
  <section class="report-section">
    <div class="report-formno">Form 3</div>
    <div class="report-title">Kertas Kerja Identifikasi Risiko</div>
    <div class="report-subtitle">{{ opdName }} — Tahun {{ tahun }}</div>
    <table class="rpt">
      <thead><tr><th style="width: 28px">No</th><th>Tujuan/Sasaran/Kegiatan</th><th>Risiko</th><th style="width: 90px">Kode</th><th>Pemilik</th><th>Sebab</th><th style="width: 40px">C/UC</th><th>Dampak</th></tr></thead>
      <tbody>
        <template v-for="g in data" :key="g.jenis">
          <tr><td class="c"></td><td colspan="7"><b>{{ jenisLabel[g.jenis] }}</b></td></tr>
          <tr v-for="(it, i) in g.items" :key="it.id">
            <td class="c">{{ i + 1 }}</td><td>{{ it.kegiatan || it.tujuan_sasaran }}</td><td>{{ it.uraian_risiko }}</td>
            <td>{{ it.kode_risiko }}</td><td>{{ it.pemilik_risiko }}</td><td>{{ it.sebab_uraian }}</td>
            <td class="c">{{ it.cuc }}</td><td>{{ it.dampak_uraian }}</td>
          </tr>
          <tr v-if="!g.items.length"><td class="c"></td><td colspan="7" class="c">Belum ada data</td></tr>
        </template>
      </tbody>
    </table>
  </section>
</template>
