"""GraphQL queries for OpenCTI API."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CollectionQuery:
    """Metadata for a predefined collection query."""

    result_key: str
    label: str
    query: str


# Collection queries for various STIX Domain Objects
COLLECTION_QUERIES: dict[str, CollectionQuery] = {
    "indicators": CollectionQuery(
        result_key="indicators",
        label="OpenCTI indicators",
        query="""
query Indicators($search: String, $first: Int) {
  indicators(search: $search, first: $first) {
    edges {
      node {
        id
        standard_id
        entity_type
        name
        description
        confidence
        pattern_type
        pattern
        indicator_types
        valid_from
        valid_until
        x_opencti_score
        created
        modified
        created_at
        updated_at
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
""",
    ),
    "threat_actors": CollectionQuery(
        result_key="threatActors",
        label="OpenCTI threat actors",
        query="""
query ThreatActors($search: String, $first: Int) {
  threatActors(search: $search, first: $first) {
    edges {
      node {
        id
        standard_id
        entity_type
        name
        description
        aliases
        threat_actor_types
        first_seen
        last_seen
        roles
        goals
        sophistication
        resource_level
        primary_motivation
        secondary_motivations
        personal_motivations
        confidence
        created
        modified
        created_at
        updated_at
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
""",
    ),
    "intrusion_sets": CollectionQuery(
        result_key="intrusionSets",
        label="OpenCTI intrusion sets",
        query="""
query IntrusionSets($search: String, $first: Int) {
  intrusionSets(search: $search, first: $first) {
    edges {
      node {
        id
        standard_id
        entity_type
        name
        description
        aliases
        first_seen
        last_seen
        goals
        resource_level
        primary_motivation
        secondary_motivations
        confidence
        created
        modified
        created_at
        updated_at
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
""",
    ),
    "campaigns": CollectionQuery(
        result_key="campaigns",
        label="OpenCTI campaigns",
        query="""
query Campaigns($search: String, $first: Int) {
  campaigns(search: $search, first: $first) {
    edges {
      node {
        id
        standard_id
        entity_type
        name
        description
        aliases
        first_seen
        last_seen
        objective
        confidence
        created
        modified
        created_at
        updated_at
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
""",
    ),
    "malware": CollectionQuery(
        result_key="malwares",
        label="OpenCTI malware",
        query="""
query Malwares($search: String, $first: Int) {
  malwares(search: $search, first: $first) {
    edges {
      node {
        id
        standard_id
        entity_type
        name
        description
        aliases
        malware_types
        is_family
        first_seen
        last_seen
        architecture_execution_envs
        implementation_languages
        capabilities
        confidence
        created
        modified
        created_at
        updated_at
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
""",
    ),
    "attack_patterns": CollectionQuery(
        result_key="attackPatterns",
        label="OpenCTI attack patterns",
        query="""
query AttackPatterns($search: String, $first: Int) {
  attackPatterns(search: $search, first: $first) {
    edges {
      node {
        id
        standard_id
        entity_type
        name
        description
        aliases
        x_mitre_platforms
        x_mitre_permissions_required
        x_mitre_detection
        x_mitre_id
        confidence
        created
        modified
        created_at
        updated_at
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
""",
    ),
    "infrastructures": CollectionQuery(
        result_key="infrastructures",
        label="OpenCTI infrastructures",
        query="""
query Infrastructures($search: String, $first: Int) {
  infrastructures(search: $search, first: $first) {
    edges {
      node {
        id
        standard_id
        entity_type
        name
        description
        aliases
        infrastructure_types
        first_seen
        last_seen
        confidence
        created
        modified
        created_at
        updated_at
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
""",
    ),
    "vulnerabilities": CollectionQuery(
        result_key="vulnerabilities",
        label="OpenCTI vulnerabilities",
        query="""
query Vulnerabilities($search: String, $first: Int) {
  vulnerabilities(search: $search, first: $first) {
    edges {
      node {
        id
        standard_id
        entity_type
        name
        description
        x_opencti_base_score
        x_opencti_base_severity
        x_opencti_attack_vector
        x_opencti_integrity_impact
        x_opencti_availability_impact
        confidence
        created
        modified
        created_at
        updated_at
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
""",
    ),
    "reports": CollectionQuery(
        result_key="reports",
        label="OpenCTI reports",
        query="""
query Reports($search: String, $first: Int) {
  reports(search: $search, first: $first) {
    edges {
      node {
        id
        standard_id
        entity_type
        name
        description
        report_types
        published
        confidence
        created
        modified
        created_at
        updated_at
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
""",
    ),
    "tools": CollectionQuery(
        result_key="tools",
        label="OpenCTI tools",
        query="""
query Tools($search: String, $first: Int) {
  tools(search: $search, first: $first) {
    edges {
      node {
        id
        standard_id
        entity_type
        name
        description
        aliases
        tool_types
        tool_version
        confidence
        created
        modified
        created_at
        updated_at
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
""",
    ),
    "incidents": CollectionQuery(
        result_key="incidents",
        label="OpenCTI incidents",
        query="""
query Incidents($search: String, $first: Int) {
  incidents(search: $search, first: $first) {
    edges {
      node {
        id
        standard_id
        entity_type
        name
        description
        aliases
        first_seen
        last_seen
        objective
        incident_type
        severity
        source
        confidence
        created
        modified
        created_at
        updated_at
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
""",
    ),
}


# Entity retrieval queries
CORE_OBJECT_QUERY = """
query GetCoreObject($id: String!) {
  stixCoreObject(id: $id) {
    id
    standard_id
    entity_type
    parent_types
    spec_version
    created_at
    updated_at
    representative {
      main
      secondary
    }
    x_opencti_stix_ids
    ... on StixDomainObject {
      created
      modified
      revoked
      confidence
      lang
    }
    ... on Container {
      created
      modified
    }
  }
}
"""

CORE_RELATIONSHIP_QUERY = """
query GetCoreRelationship($id: String!) {
  stixCoreRelationship(id: $id) {
    id
    standard_id
    entity_type
    relationship_type
    description
    start_time
    stop_time
    confidence
    created_at
    updated_at
    from {
      ... on BasicObject {
        id
        entity_type
      }
    }
    to {
      ... on BasicObject {
        id
        entity_type
      }
    }
  }
}
"""

CYBER_OBSERVABLE_QUERY = """
query GetObservable($id: String!) {
  stixCyberObservable(id: $id) {
    id
    standard_id
    entity_type
    observable_value
    created_at
    updated_at
    x_opencti_description
    x_opencti_score
    ... on DomainName {
      value
    }
    ... on IPv4Addr {
      value
    }
    ... on IPv6Addr {
      value
    }
    ... on StixFile {
      name
      size
      mime_type
      hashes {
        algorithm
        hash
      }
    }
    ... on Artifact {
      url
      mime_type
      hashes {
        algorithm
        hash
      }
    }
  }
}
"""

# Relationship queries
ENTITY_RELATIONSHIPS_QUERY = """
query GetEntityRelationships($id: String!, $first: Int) {
  stixCoreObject(id: $id) {
    id
    entity_type
    stixCoreRelationships(first: $first) {
      edges {
        node {
          id
          entity_type
          relationship_type
          description
          start_time
          stop_time
          confidence
          created
          from {
            ... on BasicObject {
              id
              entity_type
            }
            ... on BasicRelationship {
              id
              entity_type
            }
          }
          to {
            ... on BasicObject {
              id
              entity_type
            }
            ... on BasicRelationship {
              id
              entity_type
            }
          }
        }
      }
    }
  }
}
"""

# Entity-specific queries
ENTITY_INDICATORS_QUERY = """
query GetEntityIndicators($id: String!, $first: Int) {
  stixCoreObject(id: $id) {
    id
    entity_type
    stixCoreRelationships(
      relationship_type: "indicates"
      first: $first
    ) {
      edges {
        node {
          id
          to {
            ... on Indicator {
              id
              standard_id
              entity_type
              name
              description
              pattern_type
              pattern
              indicator_types
              valid_from
              valid_until
              x_opencti_score
              confidence
              created
              modified
            }
          }
        }
      }
    }
  }
}
"""

ENTITY_ATTACK_PATTERNS_QUERY = """
query GetEntityAttackPatterns($id: String!, $first: Int) {
  stixCoreObject(id: $id) {
    id
    entity_type
    stixCoreRelationships(
      relationship_type: "uses"
      first: $first
    ) {
      edges {
        node {
          id
          to {
            ... on AttackPattern {
              id
              standard_id
              entity_type
              name
              description
              aliases
              x_mitre_platforms
              x_mitre_permissions_required
              x_mitre_detection
              x_mitre_id
              confidence
              created
              modified
            }
          }
        }
      }
    }
  }
}
"""

ENTITY_OBSERVABLES_QUERY = """
query GetEntityObservables($id: String!, $first: Int) {
  stixCoreObject(id: $id) {
    id
    entity_type
    stixCoreRelationships(
      relationship_type: "related-to"
      first: $first
    ) {
      edges {
        node {
          id
          to {
            ... on StixCyberObservable {
              id
              standard_id
              entity_type
              observable_value
              x_opencti_score
              x_opencti_description
              created_at
              updated_at
            }
          }
        }
      }
    }
  }
}
"""

ENTITY_NOTES_QUERY = """
query GetEntityNotes($id: String!, $first: Int) {
  stixCoreObject(id: $id) {
    id
    entity_type
    notes(first: $first) {
      edges {
        node {
          id
          standard_id
          entity_type
          attribute_abstract
          content
          authors
          confidence
          created
          modified
          created_at
          updated_at
        }
      }
    }
  }
}
"""

SEARCH_BY_STIX_ID_QUERY = """
query SearchByStixId($stixId: StixRef!) {
  stixDomainObject(id: $stixId) {
    id
    standard_id
    entity_type
    spec_version
    created_at
    updated_at
    ... on StixDomainObject {
      created
      modified
      revoked
      confidence
      lang
    }
  }
}
"""

LIST_CONNECTORS_QUERY = """
query ListConnectors {
  connectors {
    id
    name
    connector_type
    connector_scope
    active
    auto
    created_at
    updated_at
  }
}
"""

MALWARE_ANALYSIS_QUERY = """
query GetMalwareAnalysis($id: String!) {
  malware(id: $id) {
    id
    standard_id
    entity_type
    name
    description
    aliases
    malware_types
    is_family
    first_seen
    last_seen
    architecture_execution_envs
    implementation_languages
    capabilities
    confidence
    killChainPhases {
      edges {
        node {
          id
          kill_chain_name
          phase_name
        }
      }
    }
    stixCoreRelationships {
      edges {
        node {
          id
          relationship_type
          from {
            ... on BasicObject {
              id
              entity_type
            }
          }
          to {
            ... on BasicObject {
              id
              entity_type
            }
          }
        }
      }
    }
    created
    modified
    created_at
    updated_at
  }
}
"""
