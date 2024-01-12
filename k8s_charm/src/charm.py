#!/usr/bin/env python3

import logging

import ops

from charms.data_platform_libs.v0 import data_interfaces

LOG = logging.getLogger(__name__)


class DatabaseNotReady(Exception):
    pass


class MongoWebappSampleCharm(ops.CharmBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pebble_service_name = "mongo-webapp-service"
        self.container = self.unit.get_container("web-server")

        # The 'relation_name' comes from the 'metadata.yaml file'.
        # The 'database_name' is the name of the database that our
        # application requires.
        self.database = data_interfaces.DatabaseRequires(
            self, relation_name="database", database_name="sample_app")

        # The event name is based on the container name that was specified
        # in the metadata.yaml file.
        self.framework.observe(
            self.on.web_server_pebble_ready, self._update_layer_and_restart)
        self.framework.observe(
            self.on.config_changed, self._on_config_changed)

        # See https://charmhub.io/data-platform-libs/libraries/data_interfaces
        self.framework.observe(
            self.database.on.database_created, self._on_database_created)
        self.framework.observe(
            self.database.on.endpoints_changed, self._on_database_created)
        self.framework.observe(
            self.on.database_relation_broken,
            self._on_database_relation_removed)

    def _on_config_changed(self, event):
        LOG.info("Configuration changed.")
        # Update the Pebble layer and restart the application with the
        # new settings.
        self._update_layer_and_restart(None)

    def _on_database_created(self, event):
        self._update_layer_and_restart(None)

    def _on_database_relation_removed(self, event) -> None:
        # We'll allow manually configured URIs to be used.
        self._update_layer_and_restart(None)

    @property
    def _pebble_layer(self):
        """Return a dictionary representing a Pebble layer."""
        entry_point = "mongo_webapp_sample.cmd.api:register_app()"
        listen_addr = "0.0.0.0"
        listen_port = self.config['port']
        worker_count = self.config['workers']
        command = (
            f"gunicorn -b {listen_addr}:{listen_port} "
            f"-w {worker_count} '{entry_point}'")

        mongo_url = self.config['mongo_url']
        try:
            db_data = self._fetch_mongo_relation_data()
            mongo_url = db_data['uris']
        except DatabaseNotReady:
            if mongo_url:
                LOG.info("Database relation not available yet, using "
                         "manually configured URL.")
            else:
                # reraise if there's no manually configured MongoDB url to
                # use as fallback.
                LOG.info("No database relation or manually "
                         "configured MongoDB URL.")
                raise

        env_vars = {
            "SAMPLEAPP_MONGO_URL": mongo_url,
            "SAMPLEAPP_MONGO_DB_NAME": self.config['mongo_db_name'],
            "SAMPLEAPP_DEBUG": self.config['debug'],
            "SAMPLEAPP_MONGO_CONN_TIMEOUT": self.config['mongo_conn_timeout'],
            "SAMPLEAPP_MONGO_OP_TIMEOUT": self.config['mongo_op_timeout'],
        }

        pebble_layer = {
            "summary": "Mongo webapp service",
            "description": "pebble config layer for Mongo webapp sample",
            "services": {
                self.pebble_service_name: {
                    "override": "replace",
                    "summary": "Mongo webapp service",
                    "command": command,
                    "startup": "enabled",
                    "environment": env_vars,
                }
            },
        }
        return ops.pebble.Layer(pebble_layer)

    def _update_layer_and_restart(self, event):
        self.unit.status = ops.MaintenanceStatus("Assembling pod spec")
        if self.container.can_connect():
            try:
                new_layer = self._pebble_layer.to_dict()
            except DatabaseNotReady:
                self.unit.status = ops.WaitingStatus(
                    "Waiting for MongoDB endpoint.")
                return

            # Get the current pebble layer config
            services = self.container.get_plan().to_dict().get("services", {})
            if services != new_layer["services"]:
                # Changes were made, add the new layer
                self.container.add_layer(
                    "mongodb_webapp_sample",
                    self._pebble_layer, combine=True)
                LOG.info("Added updated layer 'mongodb_webapp_sample' "
                         "to Pebble plan")

                self.container.restart(self.pebble_service_name)
                LOG.info(f"Restarted '{self.pebble_service_name}' service")

            self.unit.status = ops.ActiveStatus()
        else:
            self.unit.status = ops.WaitingStatus(
                "Waiting for Pebble in workload container")

    def _fetch_mongo_relation_data(self):
        """Fetch MongoDB relation data."""
        relations = self.database.fetch_relation_data()
        LOG.debug("Got following database data: %s", relations)
        for data in relations.values():
            if not data:
                continue
            if not data.get("uris"):
                LOG.info("MongoDB URIs not available yet.")
                continue

            db_data = {
                "uris": data["uris"],
            }
            return db_data
        raise DatabaseNotReady()


if __name__ == "__main__":
    ops.main(MongoWebappSampleCharm)
