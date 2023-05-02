#!/bin/bash
#
# Sets up enviroment for dev in local dev container.
set -e

echo "Setting up dev container ..."

# Skip when called in a github action workflow
if [[ ${CI} != "true" ]]; then
	echo "Adding local SSH keys ..."
	# Add local SSH private keys in order to push to github from the dev container
	ssh-add
fi

echo "Done setting up dev container"
