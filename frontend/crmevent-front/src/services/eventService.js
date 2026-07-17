import api from "@/api/api";

export function getEvents() {
  return api.get("/events");
}

export function getEvent(id) {
  return api.get(`/events/${id}`);
}