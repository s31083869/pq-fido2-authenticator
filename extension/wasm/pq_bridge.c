#include <limits.h>
#include <stddef.h>
#include <stdint.h>

#include <oqs/oqs.h>

#ifndef EMSCRIPTEN_KEEPALIVE
#define EMSCRIPTEN_KEEPALIVE __attribute__((used))
#endif

/*
 * 把 COSE 演算法編號翻成 liboqs 的演算法名稱，供 OQS_SIG_new() 建立簽章器。
 *
 * 對應必須和共用演算法表 shared/pq-algorithms.json 的 oqsName 相同（決策 D3）；C 不能讀 JSON，
 * 一致性由 extension/src/background/liboqs-wasm-bridge.test.ts 的 T1 檢查（WASM 回報的大小等於共用表）。
 * -48/-49/-50：ML-DSA-44/65/87（RFC 9964、FIPS 204）。
 * -54/-55：FN-DSA-512/1024 的暫定 COSE 編號（決策 D1），使用 Falcon 第三輪規格 v1.2 的
 *          不補滿格式 Falcon-512/1024（決策 D2），不是 Falcon-padded-512/1024。
 *
 * 輸入：COSE 演算法編號。
 * 輸出：liboqs 名稱；不支援的編號回傳 NULL，呼叫端再回傳 -1。
 * 注意：名稱對應到的演算法還必須編進 liboqs.a（setup-liboqs-emscripten.sh 的 LIBOQS_MINIMAL_BUILD），
 *       否則 OQS_SIG_new() 回傳 NULL，呼叫端回傳 -2。
 */
static const char *pq_alg_name(int32_t cose_alg) {
    switch (cose_alg) {
        case -48:
            return "ML-DSA-44";
        case -49:
            return "ML-DSA-65";
        case -50:
            return "ML-DSA-87";
        case -54:
            return "Falcon-512";
        case -55:
            return "Falcon-1024";
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
