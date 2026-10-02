# Object storage operations

Source: https://docs.portworx.com/portworx-enterprise/operations/operate-kubernetes/storage-operations/object (Portworx Enterprise 3.6)

Object storage operations | Portworx Enterprise Documentation

Skip to main content

EARLY ACCESS

This feature is available as Early Access (EA) and should not be used in production.

Version: 3.7

## Overview​

Portworx Object Service allows storage admins to provision object storage buckets with various backing providers using custom Kubernetes objects. You control this provisioning with a set of `CustomResourceDefinition` entries that are managed by Stork, which are as follows:

- PXBucketClass

- PXBucketClaim

- PXBucketAccess

## Supported object services​

Portworx Object Service provides an abstraction to use any object backend through Kubernetes. The following object backends are supported during early access:

-
Pure FlashBlade

-
AWS S3

important

Ensure that your object store is compatible with AWS SDK v2. Portworx uses SDK v2 starting with version 3.4.1, following the end of life (EOL) of SDK v1. While Portworx is fully S3-compliant as a client, SDK v2 includes stricter data integrity checks that are enabled by default. Some object storage systems, such as older versions of MinIO or other S3-compatible backends may not fully support these checks and can cause compatibility issues.

Proceed to one of the following sections about Portworx Object Service operations.

## 📄 Install Portworx Object service

This guide is a step-by-step tutorial on how to install the Portworx Object Service.

## 📄 Create buckets

This guide is a step-by-step tutorial on how to provision buckets with Portworx.

## 📄 Import existing buckets

This guide is a step-by-step tutorial on how to import existing buckets with Portworx.

## 📄 Application setup with bucket access

This guide is a step-by-step tutorial on how to use buckets with your applications.

## 📄 Custom Resource Definitions

Documentation for all Portworx Custom Resource Definitions (CRDs).

In this topic:
