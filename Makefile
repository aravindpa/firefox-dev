# Makefile for source rpm: firefox
# $Id$
NAME := firefox
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
