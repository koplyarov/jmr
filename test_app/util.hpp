#ifndef TEST_APP_UTIL_HPP
#define TEST_APP_UTIL_HPP


#include <joint.cpp/String.hpp>


inline std::vector<joint::String> SplitString(const joint::String& str, char delim)
{
    std::vector<joint::String> result;
    auto storage = str.Storage();

    std::string word;
    for (auto byte : storage)
    {
        if (byte != delim)
        {
            word.push_back(byte);
            continue;
        }

        if (!word.empty())
        {
            result.push_back(joint::String(word));
            word.clear();
        }
    }

    if (!word.empty())
        result.push_back(joint::String(word));

    return result;
}



#endif
