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
    url: '/api/mysql/product',
    method: 'get',
    params
  })
}

export function mysql_movie(params) {
  return request({
    url: '/api/mysql/movie',
    method: 'get',
    params
  })
}

export function mysql_sql(params) {
  return request({
    url: '/api/mysql/sql',
    method: 'get',
    params
  })
}

export function neo4j_product(params) {
  return request({
    url: '/api/mysql/product',
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
