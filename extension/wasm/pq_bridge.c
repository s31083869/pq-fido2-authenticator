#include <limits.h>
#include <stddef.h>
#include <stdint.h>

#include <oqs/oqs.h>

#ifndef EMSCRIPTEN_KEEPALIVE
#define EMSCRIPTEN_KEEPALIVE __attribute__((used))
#endif

static const char *pq_alg_name(int32_t cose_alg) {
    switch (cose_alg) {
        case -48:
            return "ML-DSA-44";
        case -49:
            return "ML-DSA-65";
        case -50:
            return "ML-DSA-87";
        default:
            return NULL;
    }
}

EMSCRIPTEN_KEEPALIVE int32_t pq_public_key_bytes(int32_t cose_alg) {
    const char *alg = pq_alg_name(cose_alg);
    if (alg == NULL) {
        return -1;
    }

    OQS_SIG *sig = OQS_SIG_new(alg);
    if (sig == NULL) {
        return -2;
    }

    int32_t out = (int32_t)sig->length_public_key;
    OQS_SIG_free(sig);
    return out;
}

EMSCRIPTEN_KEEPALIVE int32_t pq_secret_key_bytes(int32_t cose_alg) {
    const char *alg = pq_alg_name(cose_alg);
    if (alg == NULL) {
        return -1;
    }

    OQS_SIG *sig = OQS_SIG_new(alg);
    if (sig == NULL) {
        return -2;
    }

    int32_t out = (int32_t)sig->length_secret_key;
    OQS_SIG_free(sig);
    return out;
}

EMSCRIPTEN_KEEPALIVE int32_t pq_signature_bytes(int32_t cose_alg) {
    const char *alg = pq_alg_name(cose_alg);
    if (alg == NULL) {
        return -1;
    }

    OQS_SIG *sig = OQS_SIG_new(alg);
    if (sig == NULL) {
        return -2;
    }

    int32_t out = (int32_t)sig->length_signature;
    OQS_SIG_free(sig);
    return out;
}

EMSCRIPTEN_KEEPALIVE int32_t pq_generate_keypair(int32_t cose_alg, uint8_t *public_key_out,
                                                 uint8_t *secret_key_out) {
    const char *alg = pq_alg_name(cose_alg);
    if (alg == NULL) {
        return -1;
    }

    OQS_SIG *sig = OQS_SIG_new(alg);
    if (sig == NULL) {
        return -2;
    }

    OQS_STATUS status = OQS_SIG_keypair(sig, public_key_out, secret_key_out);
    OQS_SIG_free(sig);

    return status == OQS_SUCCESS ? 0 : -3;
}

EMSCRIPTEN_KEEPALIVE int32_t pq_sign(int32_t cose_alg, const uint8_t *secret_key,
                                     uint32_t secret_key_len, const uint8_t *message,
                                     uint32_t message_len, uint8_t *signature_out,
                                     uint32_t signature_capacity,
                                     uint32_t *signature_len_out) {
    const char *alg = pq_alg_name(cose_alg);
    if (alg == NULL) {
        return -1;
    }

    OQS_SIG *sig = OQS_SIG_new(alg);
    if (sig == NULL) {
        return -2;
    }

    if (secret_key_len != (uint32_t)sig->length_secret_key) {
        OQS_SIG_free(sig);
        return -4;
    }

    if (signature_capacity < (uint32_t)sig->length_signature) {
        OQS_SIG_free(sig);
        return -5;
    }

    size_t actual_len = 0;
    OQS_STATUS status =
        OQS_SIG_sign(sig, signature_out, &actual_len, message, (size_t)message_len, secret_key);
    OQS_SIG_free(sig);

    if (status != OQS_SUCCESS) {
        return -3;
    }

    if (actual_len > UINT32_MAX) {
        return -6;
    }

    *signature_len_out = (uint32_t)actual_len;
    return 0;
}
