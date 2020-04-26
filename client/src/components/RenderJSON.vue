<template>
  <b-container fluid>
    <b-pagination v-model="currentPage" :total-rows="rows" :per-page="perPage" aria-controls="my-table"></b-pagination>
    <b-form-group id="input-group-perPage" label="Number of elements per page: " label-for="input-field-perPage">
      <b-form-input id="input-field-perPage" v-model="perPage"></b-form-input>
    </b-form-group>
    <b-form-group id="input-group-size" label="Number of elements to fetch: " label-for="input-field-size">
      <b-form-input id="input-field-size" v-model="size"></b-form-input>
    </b-form-group>
    <b-form-group id="input-group-button">
      <b-button variant="primary" id="input-field-button" @click="getData">Fetch</b-button>
    </b-form-group>
    <b-form-group label="Filter (supports regex)" label-for="filterInput">
      <b-input-group>
        <b-form-input v-model="filter" type="search" id="filterInput" placeholder="Type to Search"></b-form-input>
        <b-input-group-append>
          <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
        </b-input-group-append>
      </b-input-group>
    </b-form-group>
    <b-form-group label="Filter on: " label-for="initialSortSelect">
      <b-form-select v-model="filterOn" id="initialSortSelect" :options="filterOptions"></b-form-select>
    </b-form-group>
    <b-table :filterIncludedFields="filterOn" @filtered="onFiltered" :filter="searchRegex" id="my-table" :items="alerts" :per-page="perPage" :current-page="currentPage" striped hover :fields="fields" @row-clicked="item=>$set(item, '_showDetails', !item._showDetails)">
      <template v-slot:row-details="row">
        <vue-code-highlight language="json">{{ row.item }}</vue-code-highlight>
      </template>
    </b-table>
  </b-container>
</template>

<script>

import { component as VueCodeHighlight } from 'vue-code-highlight';
import axios from 'axios'

const basePath = '/api'

export default {
  name: 'RenderJSON',
  components:{
    VueCodeHighlight
  },
  computed: {
    rows() {
      return this.alerts.length
    },
    searchRegex() {
      return new RegExp(this.filter)
    }
  },
  data () {
    return {
      fields: [
        {
          key: 'timestamp',
          sortable: true
        },
        {
          key: 'src_ip',
          sortable: true
        },
        {
          key: 'src_port',
          sortable: true
        },
        {
          key: 'dest_ip',
          sortable: true
        },
        {
          key: 'dest_port',
          sortable: true
        },
        {
          key: 'proto',
          sortable: true
        },
        {
          key: 'alert.signature',
          sortable: true
        }
      ],
      filterOptions: [
        { value: null, text: 'All' },
        { value: 'timestamp', text: 'Timestamp' },
        { value: 'src_ip', text: 'Source IP' },
        { value: 'src_port', text: 'Source port' },
        { value: 'dest_ip', text: 'Destination IP' },
        { value: 'dest_port', text: 'Destination port' },
        { value: 'proto', text: 'Protocol' },
        { value: 'alert.signature', text: 'Signature' },
        { value: 'app_proto', text: 'Application protocol' }
      ],
      filter: '',
      filterOn: '',
      perPage: 10,
      currentPage: 1,
      size: 10,
      alerts: []
    }
  },
  methods: {
    getData () {
      const path = basePath + '/eve?size=' + this.size
      axios.get (path)
        .then (response => {
          this.alerts = response.data.alerts
        })
        .catch (error => {
          console.log(error)
        })
    },
    onFiltered(filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length
      this.currentPage = 1
    }
  },
  created () {
    this.getData ()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
