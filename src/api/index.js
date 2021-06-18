import request from '@/utils/request'

export function find_organization(params) {
  return request({
    url: '/api/organization',
    method: 'get',
    params
  })
}

export function neo4j_sql(params) {
  return request({
    url: '/api/query',
    params
  })
}

export function neo4j_org(hasPermId) {
  return request({
    url: '/api/query',
    params: { cypher: `MATCH (n:Organization) WHERE n.hasPermId="${hasPermId}" RETURN n LIMIT 1` }
  })
}

export function neo4j_psn(hasPermId) {
  return request({
    url: '/api/query',
    params: { cypher: `MATCH (n:Person) WHERE n.hasPermId="${hasPermId}" RETURN n LIMIT 1` }
  })
}

export function combine_product() {
  return {};
}
