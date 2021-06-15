import request from '@/utils/request'

export function combine_product(params) {
  return request({
    url: '/api/combine/product',
    method: 'get',
    params
  })
}

export function mysql_product(params) {
  return request({
    url: '/api/product',
    method: 'get',
    params
  })
}

export function find_organization(params) {
  return request({
    url: '/api/organization',
    method: 'get',
    params
  })
}

export function mysql_sql(params) {
  return request({
    url: '/api/sql',
    method: 'get',
    params
  })
}

export function neo4j_product(params) {
  return request({
    url: '/api/product',
    method: 'get',
    params
  })
}

export function neo4j_relation(params) {
  return request({
    url: '/api/neo4j/relation',
    method: 'get',
    params
  })
}

export function neo4j_sql(params) {
  return request({
    url: '/api/neo4j/sql',
    method: 'get',
    params
  })
}
