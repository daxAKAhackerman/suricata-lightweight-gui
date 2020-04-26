<template>
  <b-container fluid>
    <b-pagination
      v-model="currentPage"
      :total-rows="totalRows"
      :per-page="perPage"
    ></b-pagination>
    <b-form-group
      id="input-group-perPage"
      label="Number of elements per page: "
      label-for="input-field-perPage"
    >
      <b-form-input id="input-field-perPage" v-model="perPage"></b-form-input>
    </b-form-group>
    <b-form-group
      id="input-group-size"
      label="Number of elements to fetch: "
      label-for="input-field-size"
    >
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
    <b-form-group label="Filter On" description="Leave all unchecked to filter on all data">
      <b-form-checkbox-group v-model="filterOn">
        <b-form-checkbox value="timestamp">Timestamp</b-form-checkbox>
        <b-form-checkbox value="src_ip">Source IP</b-form-checkbox>
        <b-form-checkbox value="src_port">Source port</b-form-checkbox>
        <b-form-checkbox value="dest_ip">Destination IP</b-form-checkbox>
        <b-form-checkbox value="dest_port">Destination port</b-form-checkbox>
        <b-form-checkbox value="proto">Protocol</b-form-checkbox>
        <b-form-checkbox value="alert.signature">Signature</b-form-checkbox>
        <b-form-checkbox value="app_proto">Application protocol</b-form-checkbox>
      </b-form-checkbox-group>
    </b-form-group>
    <b-table
      :filterIncludedFields="filterOn"
      @filtered="onFiltered"
      :filter="searchRegex"
      id="my-table"
      :items="alerts"
      :per-page="perPage"
      :current-page="currentPage"
      striped
      hover
      :fields="fields"
      @row-clicked="item=>$set(item, '_showDetails', !item._showDetails)"
    >
      <template v-slot:row-details="row">
        <vue-code-highlight language="json">{{ row.item }}</vue-code-highlight>
      </template>
      <template v-slot:cell(src_ip)="row">
        <b-link :href="'https://www.virustotal.com/gui/ip-address/' + row.item.src_ip + '/detection'">{{ row.item.src_ip }}</b-link>
      </template>
      <template v-slot:cell(dest_ip)="row">
        <b-link :href="'https://www.virustotal.com/gui/ip-address/' + row.item.dest_ip + '/detection'">{{ row.item.dest_ip }}</b-link>
      </template>
    </b-table>
  </b-container>
</template>

<script>
import { component as VueCodeHighlight } from "vue-code-highlight";
import axios from "axios";

const basePath = "/api";

export default {
  name: "RenderJSON",
  components: {
    VueCodeHighlight
  },
  mounted () {
    this.totalRows = this.alerts.length
  },
  computed: {
    searchRegex() {
      return new RegExp(this.filter);
    }
  },
  data() {
    return {
      fields: [
        {
          key: "timestamp",
          sortable: true
        },
        {
          key: "src_ip",
          sortable: true
        },
        {
          key: "src_port",
          sortable: true
        },
        {
          key: "dest_ip",
          sortable: true
        },
        {
          key: "dest_port",
          sortable: true
        },
        {
          key: "proto",
          sortable: true
        },
        {
          key: "alert.signature",
          sortable: true
        }
      ],
      filter: "",
      filterOn: [],
      perPage: 10,
      currentPage: 1,
      size: 10,
      alerts: [],
      totalRows: 0
    };
  },
  methods: {
    getData() {
      const path = basePath + "/eve?size=" + this.size;
      axios
        .get(path)
        .then(response => {
          this.alerts = response.data.alerts;
        })
        .catch(error => {
          console.log(error);
        });
    },
    onFiltered(filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length
    }
  },
  created() {
    this.getData();
  }
};
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
